package ws

import (
	"bufio"
	"encoding/json"
	"fmt"
	"io"
	"log/slog"
	"net/http"
	"os/exec"
	"strings"

	"github.com/go-chi/chi/v5"
	"github.com/gorilla/websocket"
)

// SandboxConfig holds configuration for the sandbox WebSocket handler.
type SandboxConfig struct {
	ContainerName string
	ShellCmd      string
}

// SandboxHandler manages WebSocket ↔ container connections for the study page.
// Supports multiple endpoints:
//   - /sandbox/playground — Alpine shell (docker exec /bin/sh)
//   - /sandbox/vtysh     — FRRouting VTYSH CLI (docker exec vtysh)
//   - /sandbox/junos     — cRPD JunOS CLI (docker exec cli)
type SandboxHandler struct {
	containerName string
	shellCmd      string
}

// NewSandboxHandler creates a new sandbox handler with default config.
func NewSandboxHandler(cfg *SandboxConfig) *SandboxHandler {
	if cfg == nil {
		cfg = &SandboxConfig{}
	}
	containerName := cfg.ContainerName
	if containerName == "" {
		containerName = "netcert-staging-sandbox"
	}
	shellCmd := cfg.ShellCmd
	if shellCmd == "" {
		shellCmd = "/bin/sh"
	}
	return &SandboxHandler{
		containerName: containerName,
		shellCmd:      shellCmd,
	}
}

// RegisterRoutes registers WebSocket routes on a chi router.
func (h *SandboxHandler) RegisterRoutes(r chi.Router) {
	r.Get("/sandbox/playground", h.handlePlayground)
	r.Get("/sandbox/vtysh", h.handleVTYSH)
	r.Get("/sandbox/junos", h.handleJunOS)
}

// --- Docker exec bridge ---

// dockerExecBridge upgrades HTTP to WebSocket and bridges to a docker exec session.
// container: name of the container to exec into
// execCmd: command to run inside the container (e.g. "/bin/sh", "vtysh", "cli")
// welcomeMsg: optional welcome message shown on connect
// containerLabel: human-readable label for error messages (e.g. "FRR", "cRPD")
func dockerExecBridge(w http.ResponseWriter, r *http.Request, container, execCmd, welcomeMsg, containerLabel string) {
	conn, err := upgrader.Upgrade(w, r, nil)
	if err != nil {
		slog.Error("Sandbox WebSocket upgrade failed",
			slog.String("label", containerLabel),
			slog.String("error", err.Error()))
		return
	}
	defer conn.Close()

	cmd := exec.Command("docker", "exec", "-i", container, execCmd)
	stdin, err := cmd.StdinPipe()
	if err != nil {
		writeWS(conn, fmt.Sprintf("ERROR: Failed to create stdin pipe for %s\\r\\n", containerLabel))
		return
	}
	stdout, err := cmd.StdoutPipe()
	if err != nil {
		writeWS(conn, fmt.Sprintf("ERROR: Failed to create stdout pipe for %s\\r\\n", containerLabel))
		return
	}
	stderr, err := cmd.StderrPipe()
	if err != nil {
		writeWS(conn, fmt.Sprintf("ERROR: Failed to create stderr pipe for %s\\r\\n", containerLabel))
		return
	}

	if err := cmd.Start(); err != nil {
		writeWS(conn, fmt.Sprintf("ERROR: %s container '%s' is not running.\\r\\n", containerLabel, container))
		if containerLabel == "cRPD" {
			writeWS(conn, "To enable JunOS CLI: pull crpd:24.2R1 from Juniper Support Portal and run:\\r\\n")
			writeWS(conn, "  docker compose -f infra/docker-compose.staging.yml -p netcert-staging run --rm clab-dind /labs/playground/deploy-playground.sh\\r\\n")
		} else if containerLabel == "FRR" {
			writeWS(conn, "Start it with: docker compose -f infra/docker-compose.staging.yml up -d frr\\r\\n")
		} else {
			writeWS(conn, fmt.Sprintf("Start it with: docker compose -f infra/docker-compose.staging.yml up -d %s\\r\\n", container))
		}
		return
	}
	defer cmd.Wait()

	// Send welcome message — send as-is, terminal handles \\r\\n correctly
	if welcomeMsg != "" {
		conn.WriteMessage(websocket.TextMessage, []byte(welcomeMsg))
	}

	// WebSocket → docker stdin
	go func() {
		defer stdin.Close()
		for {
			_, msg, err := conn.ReadMessage()
			if err != nil {
				return
			}
			line := string(msg)
			io.WriteString(stdin, line)
			if !strings.HasSuffix(line, "\n") {
				io.WriteString(stdin, "\n")
			}
		}
	}()

	// docker stdout+stderr → WebSocket (merge both)
	reader := io.MultiReader(stdout, stderr)
	scanner := bufio.NewScanner(reader)
	scanner.Buffer(make([]byte, 64*1024), 64*1024)
	for scanner.Scan() {
		data := scanner.Bytes()
		conn.WriteMessage(websocket.BinaryMessage, append(data, '\n'))
	}
}

// --- Handlers ---

// handlePlayground connects to the Alpine sandbox container (/bin/sh).
func (h *SandboxHandler) handlePlayground(w http.ResponseWriter, r *http.Request) {
	welcome := fmt.Sprintf(
		"\\x1b[32m┌─────────────────────────────────────────────┐\\x1b[0m\n"+
			"\\x1b[32m│  \\x1b[1mNetCert Study Sandbox\\x1b[22m  \\x1b[32m                  │\\x1b[0m\n"+
			"\\x1b[32m│  \\x1b[33mПрактикуйте Linux/network команды\\x1b[32m         │\\x1b[0m\n"+
			"\\x1b[32m│  \\x1b[90mType \\x1b[37mhelp\\x1b[90m for available commands\\x1b[32m           │\\x1b[0m\n"+
			"\\x1b[32m└─────────────────────────────────────────────┘\\x1b[0m\n\n"+
			"\\x1b[90mAlpine Linux sandbox — bash, ping, curl, tcpdump, iproute2\\x1b[0m\n"+
			"\\x1b[90mWant JunOS CLI? Use \\x1b[33mLive (cRPD)\\x1b[90m button instead\\x1b[0m\n",
	)
	dockerExecBridge(w, r, h.containerName, h.shellCmd, welcome, "Sandbox")
}

// handleVTYSH connects to the FRRouting container (vtysh).
// FRR provides a real routing CLI: show ip route, show bgp, configure terminal, etc.
func (h *SandboxHandler) handleVTYSH(w http.ResponseWriter, r *http.Request) {
	welcome :=
		"\x1b[32m┌─────────────────────────────────────────────┐\x1b[0m\n" +
			"\x1b[32m│  \x1b[1mFRRouting (FRR) Routing CLI\x1b[22m  \x1b[32m            │\x1b[0m\n" +
			"\x1b[32m│  \x1b[33mПрактикуйте show-команды и конфигурацию\x1b[32m   │\x1b[0m\n" +
			"\x1b[32m│  \x1b[90mКоманды: \\x1b[37mshow ip route\\x1b[90m, \\x1b[37mshow bgp\\x1b[90m, \\x1b[37mconf t\\x1b[90m     │\x1b[0m\n" +
			"\x1b[32m│  \x1b[90mВыйти: \\x1b[37mexit\\x1b[90m или \\x1b[37mCtrl+D\\x1b[90m                     │\x1b[0m\n" +
			"\x1b[32m└─────────────────────────────────────────────┘\x1b[0m\n\n"
	dockerExecBridge(w, r, "netcert-staging-frr", "vtysh", welcome, "FRR")
}

// handleJunOS connects to the cRPD playground container (JunOS CLI).
// Requires crpd:24.2R1 deployed via containerlab.
func (h *SandboxHandler) handleJunOS(w http.ResponseWriter, r *http.Request) {
	welcome :=
		"\x1b[32m┌─────────────────────────────────────────────┐\x1b[0m\n" +
			"\x1b[32m│  \x1b[1mJunOS Playground (cRPD)\x1b[22m  \x1b[32m               │\x1b[0m\n" +
			"\x1b[32m│  \x1b[33mРеальный JunOS CLI в вашем браузере\x1b[32m       │\x1b[0m\n" +
			"\x1b[32m│  \x1b[90mКоманды: \\x1b[37mshow interfaces\\x1b[90m, \\x1b[37mconfigure\\x1b[90m, \\x1b[37mshow route\\x1b[90m │\x1b[0m\n" +
			"\x1b[32m│  \x1b[90mВойти: admin / пароль: NetCert123\x1b[32m            │\x1b[0m\n" +
			"\x1b[32m└─────────────────────────────────────────────┘\x1b[0m\n\n"
	dockerExecBridge(w, r, "clab-playground-r1", "cli", welcome, "cRPD")
}

// --- Status endpoint ---

// SandboxStatusResponse represents the health status of sandbox backends.
type SandboxStatusResponse struct {
	VTYSH string `json:"vtysh"`
	JunOS string `json:"junos"`
}

// dockerContainerStatus checks if a Docker container is running.
// Returns "running", "stopped", or "not_found".
// Uses the local Docker socket explicitly to bypass DOCKER_HOST env (which points to clab-dind).
func dockerContainerStatus(containerName string) string {
	cmd := exec.Command("docker", "-H", "unix:///var/run/docker.sock", "inspect", "--format", "{{.State.Status}}", containerName)
	out, err := cmd.Output()
	if err != nil {
		return "not_found"
	}
	status := strings.TrimSpace(string(out))
	switch status {
	case "running":
		return "running"
	case "exited", "dead", "paused", "restarting":
		return "stopped"
	default:
		return "not_found"
	}
}

// HandleStatus returns JSON with the status of sandbox backends.
// GET /api/v1/sandbox/status
func (h *SandboxHandler) HandleStatus(w http.ResponseWriter, r *http.Request) {
	resp := SandboxStatusResponse{
		VTYSH: dockerContainerStatus("netcert-staging-frr"),
		JunOS: dockerContainerStatus("clab-playground-r1"),
	}
	w.Header().Set("Content-Type", "application/json")
	json.NewEncoder(w).Encode(resp)
}
