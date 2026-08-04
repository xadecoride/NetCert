package ws

import (
	"bufio"
	"context"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os/exec"
	"strings"
	"sync"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/google/uuid"
	"github.com/gorilla/websocket"
	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/middleware"
	"golang.org/x/crypto/ssh"
)

// defaultUpgrader is the package-level WebSocket upgrader config.
// It is replaced by SetAllowedOrigins() with origin-restricted validation.
var upgrader = defaultUpgrader()

// defaultUpgrader returns a lenient upgrader for dev use.
func defaultUpgrader() websocket.Upgrader {
	return websocket.Upgrader{
		ReadBufferSize:  4096,
		WriteBufferSize: 4096,
		CheckOrigin: func(r *http.Request) bool {
			return true // Allow all origins for dev; restrict in production
		},
	}
}

// SetAllowedOrigins replaces the package-level upgrader with one that validates
// WebSocket upgrade requests against a list of allowed origins.
// Call this during server startup before any WebSocket connections are served.
func SetAllowedOrigins(origins []string) {
	if len(origins) == 0 {
		return
	}
	allowed := make(map[string]bool, len(origins))
	for _, o := range origins {
		allowed[strings.ToLower(o)] = true
	}
	upgrader = websocket.Upgrader{
		ReadBufferSize:  4096,
		WriteBufferSize: 4096,
		CheckOrigin: func(r *http.Request) bool {
			origin := strings.ToLower(r.Header.Get("Origin"))
			// If no Origin header (same-origin request or non-browser client), allow
			if origin == "" {
				return true
			}
			return allowed[origin]
		},
	}
}

// SSHProxy manages WebSocket ↔ SSH bridge connections for lab terminals.
type SSHProxy struct {
	labUC         LabUseCaseInterface
	dindContainer string
	sshUser       string
	sshPass       string
	timeout       time.Duration
	mu            sync.RWMutex
}

// LabUseCaseInterface defines the subset of LabUseCase needed by SSHProxy.
type LabUseCaseInterface interface {
	GetSubmission(ctx context.Context, submissionID uuid.UUID, userID uuid.UUID) (*domain.LabSubmission, error)
}

// NewSSHProxy creates a new SSH proxy.
func NewSSHProxy(labUC LabUseCaseInterface, dindContainer string) *SSHProxy {
	if dindContainer == "" {
		dindContainer = "netcert-staging-clab-dind"
	}
	return &SSHProxy{
		labUC:         labUC,
		dindContainer: dindContainer,
		sshUser:       "admin",
		sshPass:       "", // cRPD default: empty password
		timeout:       10 * time.Second,
	}
}

// RegisterRoutes registers WebSocket routes on a chi router.
// Note: routes are mounted under /ws by the caller, so paths here should NOT
// include the /ws prefix (e.g. /lab/... not /ws/lab/...).
func (p *SSHProxy) RegisterRoutes(r chi.Router) {
	r.Get("/lab/{submissionID}/{deviceName}", p.handleTerminal)
	r.Get("/lab/{submissionID}/topology", p.handleTopologyUpdates)
}

// handleTerminal handles WebSocket ↔ SSH terminal connections for a lab device.
func (p *SSHProxy) handleTerminal(w http.ResponseWriter, r *http.Request) {
	submissionID := chi.URLParam(r, "submissionID")
	deviceName := chi.URLParam(r, "deviceName")

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		slog.Error("WebSocket upgrade failed", slog.String("error", err.Error()))
		return
	}
	defer conn.Close()

	// Get lab devices from submission
	subID, err := uuid.Parse(submissionID)
	if err != nil {
		slog.Error("Invalid submission ID", slog.String("submission_id", submissionID))
		writeWS(conn, "ERROR: Invalid submission ID")
		return
	}

	userID := middleware.GetUserID(r.Context())
	sub, err := p.labUC.GetSubmission(r.Context(), subID, userID)
	if err != nil || sub == nil {
		slog.Error("Submission not found", slog.String("submission_id", submissionID))
		writeWS(conn, "ERROR: Lab session not found")
		return
	}

	// Find the target device in the submission
	var targetDevice *domain.LabDevice
	for _, d := range sub.Devices {
		if d.Name == deviceName {
			targetDevice = &d
			break
		}
	}
	if targetDevice == nil {
		slog.Error("Device not found in submission",
			slog.String("device", deviceName),
			slog.String("submission_id", submissionID))
		writeWS(conn, fmt.Sprintf("ERROR: Device '%s' not found in lab", deviceName))
		return
	}

	// Strategy 1: Direct docker exec (fastest — no SSH overhead)
	containerName := fmt.Sprintf("clab-%s-%s", sub.PodID, deviceName)
	if p.tryDockerExec(conn, containerName) {
		return
	}

	// Strategy 2: SSH to device (fallback)
	slog.Info("Docker exec failed, trying SSH fallback",
		slog.String("device", deviceName),
		slog.String("mgmt_ip", targetDevice.MgmtIP))
	p.trySSH(conn, targetDevice)
}

// tryDockerExec attempts to connect via `docker exec -i` inside the DinD container.
// Returns true if successful.
func (p *SSHProxy) tryDockerExec(ws *websocket.Conn, containerName string) bool {
	// Devices run inside the DinD container, so we need to double-exec:
	// host docker → exec into DinD → docker exec into the lab device.
	cmd := exec.Command("docker", "exec", "-i", p.dindContainer, "docker", "exec", "-i", containerName, "cli")
	stdin, err := cmd.StdinPipe()
	if err != nil {
		return false
	}
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		return false
	}
	stderr, err := cmd.StderrPipe()
	if err != nil {
		return false
	}

	if err := cmd.Start(); err != nil {
		return false
	}

	// WebSocket → docker stdin
	go func() {
		defer stdin.Close()
		for {
			_, msg, err := ws.ReadMessage()
			if err != nil {
				return
			}
			// Send the raw message; the user types commands with Enter
			line := string(msg)
			io.WriteString(stdin, line)
			if !strings.HasSuffix(line, "\n") {
				io.WriteString(stdin, "\n")
			}
		}
	}()

	// docker stdout+stderr → WebSocket (merge both)
	done := make(chan struct{})
	go func() {
		reader := io.MultiReader(stdout, stderr)
		scanner := bufio.NewScanner(reader)
		scanner.Buffer(make([]byte, 64*1024), 64*1024)
		for scanner.Scan() {
			data := scanner.Bytes()
			ws.WriteMessage(websocket.BinaryMessage, append(data, '\n'))
		}
		close(done)
	}()

	// Wait for command to finish (the connection is closed externally)
	go func() {
		cmd.Wait()
		close(done)
	}()

	// Don't block — this goroutine will clean up when done
	return true
}

// trySSH attempts to connect via SSH. Returns true if successful.
func (p *SSHProxy) trySSH(ws *websocket.Conn, device *domain.LabDevice) bool {
	if device.MgmtIP == "" {
		return false
	}

	addr := fmt.Sprintf("%s:22", device.MgmtIP)
	config := &ssh.ClientConfig{
		User:            p.sshUser,
		Auth:            []ssh.AuthMethod{ssh.Password(p.sshPass)},
		// SECURITY: InsecureIgnoreHostKey accepts ANY host key. This is
		// acceptable for ephemeral lab containers inside an isolated DinD
		// network, but it exposes connections to MITM if the lab network
		// is reachable by untrusted actors. For production, consider
		// maintaining a known_hosts file per lab image.
		HostKeyCallback: ssh.InsecureIgnoreHostKey(),
		Timeout:         p.timeout,
	}

	client, err := ssh.Dial("tcp", addr, config)
	if err != nil {
		return false
	}
	defer client.Close()

	session, err := client.NewSession()
	if err != nil {
		return false
	}
	defer session.Close()

	// Request PTY for JunOS CLI
	if err := session.RequestPty("xterm-256color", 80, 24, ssh.TerminalModes{
		ssh.ECHO:          1,
		ssh.OPOST:         1,
		ssh.ONLCR:         1,
	}); err != nil {
		return false
	}

	stdin, err := session.StdinPipe()
	if err != nil {
		return false
	}
	stdout, err := session.StdoutPipe()
	if err != nil {
		return false
	}

	if err := session.Shell(); err != nil {
		return false
	}

	// WebSocket → SSH stdin
	go func() {
		defer stdin.Close()
		for {
			_, msg, err := ws.ReadMessage()
			if err != nil {
				session.Close()
				return
			}
			line := string(msg)
			io.WriteString(stdin, line)
			if !strings.HasSuffix(line, "\n") {
				io.WriteString(stdin, "\n")
			}
		}
	}()

	// SSH stdout → WebSocket
	buf := make([]byte, 32*1024)
	for {
		n, err := stdout.Read(buf)
		if err != nil {
			break
		}
		ws.WriteMessage(websocket.BinaryMessage, buf[:n])
	}

	return true
}

// handleTopologyUpdates streams real-time topology status via WebSocket.
func (p *SSHProxy) handleTopologyUpdates(w http.ResponseWriter, r *http.Request) {
	submissionID := chi.URLParam(r, "submissionID")

	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		slog.Error("Topology WS upgrade failed", slog.String("error", err.Error()))
		return
	}
	defer conn.Close()

	subID, err := uuid.Parse(submissionID)
	if err != nil {
		slog.Error("Invalid submission ID", slog.String("submission_id", submissionID))
		writeWS(conn, `{"error":"invalid submission ID"}`)
		return
	}

	userID := middleware.GetUserID(r.Context())
	sub, err := p.labUC.GetSubmission(r.Context(), subID, userID)
	if err != nil || sub == nil {
		writeWS(conn, `{"error":"submission not found"}`)
		return
	}

	// Send initial snapshot
	snapshot := map[string]interface{}{
		"type":    "topology_snapshot",
		"devices": sub.Devices,
	}
	data, _ := json.Marshal(snapshot)
	conn.WriteMessage(websocket.TextMessage, data)

	// Keep-alive loop (ping/pong)
	ticker := time.NewTicker(30 * time.Second)
	defer ticker.Stop()

	done := make(chan struct{})
	go func() {
		defer close(done)
		for {
			if _, _, err := conn.ReadMessage(); err != nil {
				return
			}
		}
	}()

	for {
		select {
		case <-done:
			return
		case <-ticker.C:
			if err := conn.WriteMessage(websocket.PingMessage, nil); err != nil {
				return
			}
		}
	}
}

// writeWS writes a text message to a WebSocket connection.
func writeWS(conn *websocket.Conn, msg string) {
	conn.WriteMessage(websocket.TextMessage, []byte(msg))
}
