package usecase

import (
	"bytes"
	"context"
	"encoding/json"
	"fmt"
	"log/slog"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"time"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

// LabRepository defines the interface for lab data access.
type LabRepository interface {
	GetByID(ctx context.Context, id uuid.UUID) (*domain.Lab, error)
	GetBySlug(ctx context.Context, slug string) (*domain.Lab, error)
	ListByTrack(ctx context.Context, trackID uuid.UUID) ([]domain.Lab, error)
	CreateSubmission(ctx context.Context, sub *domain.LabSubmission) error
	GetSubmission(ctx context.Context, id uuid.UUID) (*domain.LabSubmission, error)
	UpdateSubmissionStatus(ctx context.Context, id uuid.UUID, status domain.LabStatus, devices []domain.LabDevice, score int) error
	SaveLabScore(ctx context.Context, score *domain.LabScore) error
	GetLabScores(ctx context.Context, submissionID uuid.UUID) ([]domain.LabScore, error)
	GetActiveSubmissionsByUser(ctx context.Context, userID uuid.UUID) ([]domain.LabSubmission, error)
	CompleteSubmission(ctx context.Context, id uuid.UUID, status domain.LabStatus, finalScore int) error
}

type LabUseCase struct {
	labRepo          LabRepository
	clabBinPath      string // Path to containerlab binary
	clabDir          string // Base directory for Containerlab project files
	wsHost           string // WebSocket host for terminal proxy
	wsPort           string // WebSocket port
	labsBaseDir      string // Base directory for lab grading scripts (on disk)
	dindContainer    string // Container name for Docker-in-Docker (for grade.py execution)
	hostDockerSocket string // Path to host Docker socket for exec into DinD
}

func NewLabUseCase(labRepo LabRepository, clabBinPath, clabDir, wsHost, wsPort, labsBaseDir, dindContainer, hostDockerSocket string) *LabUseCase {
	if clabBinPath == "" {
		clabBinPath = "containerlab"
	}
	if clabDir == "" {
		clabDir = "/tmp/netcert-labs"
	}
	if wsHost == "" {
		wsHost = "0.0.0.0"
	}
	if wsPort == "" {
		wsPort = "8090"
	}
	if labsBaseDir == "" {
		labsBaseDir = "/app/labs"
	}
	if dindContainer == "" {
		dindContainer = "netcert-staging-clab-dind"
	}
	if hostDockerSocket == "" {
		hostDockerSocket = "/var/run/docker.sock"
	}
	return &LabUseCase{
		labRepo:          labRepo,
		clabBinPath:      clabBinPath,
		clabDir:          clabDir,
		wsHost:           wsHost,
		wsPort:           wsPort,
		labsBaseDir:      labsBaseDir,
		dindContainer:    dindContainer,
		hostDockerSocket: hostDockerSocket,
	}
}

// ListLabs returns all labs for a given track.
func (uc *LabUseCase) ListLabs(ctx context.Context, trackID uuid.UUID) ([]domain.Lab, error) {
	return uc.labRepo.ListByTrack(ctx, trackID)
}

// GetLab returns a single lab by ID.
func (uc *LabUseCase) GetLab(ctx context.Context, id uuid.UUID) (*domain.Lab, error) {
	return uc.labRepo.GetByID(ctx, id)
}

// StartLab deploys a Containerlab topology and creates a lab submission.
func (uc *LabUseCase) StartLab(ctx context.Context, userID uuid.UUID, req *domain.LabStartRequest) (*domain.LabSubmission, error) {
	lab, err := uc.labRepo.GetByID(ctx, req.LabID)
	if err != nil {
		return nil, fmt.Errorf("get lab: %w", err)
	}
	if lab == nil {
		return nil, fmt.Errorf("lab not found")
	}

	// Check for existing active submissions
	active, err := uc.labRepo.GetActiveSubmissionsByUser(ctx, userID)
	if err != nil {
		return nil, fmt.Errorf("check active: %w", err)
	}
	if len(active) > 0 {
		return nil, fmt.Errorf("already have active lab session: %s", active[0].ID)
	}

	submissionID := uuid.New()
	podID := fmt.Sprintf("netcert-%s-%s", lab.Slug, submissionID.String()[:8])

	// Create submission record
	sub := &domain.LabSubmission{
		ID:               submissionID,
		LabID:            lab.ID,
		UserID:           userID,
		Status:           domain.LabStatusDeploying,
		PodID:            podID,
		Devices:          []domain.LabDevice{},
		StartedAt:        time.Now().UTC(),
		TimeRemainingSec: lab.DurationMinutes * 60,
		CurrentScore:     0,
		MaxScore:         lab.MaxScore,
	}

	if err := uc.labRepo.CreateSubmission(ctx, sub); err != nil {
		return nil, fmt.Errorf("create submission: %w", err)
	}

	// Deploy Containerlab topology asynchronously
	go uc.deployTopology(submissionID, lab, podID)

	return sub, nil
}

// deployTopology runs containerlab deploy in a goroutine.
func (uc *LabUseCase) deployTopology(submissionID uuid.UUID, lab *domain.Lab, podID string) {
	ctx, cancel := context.WithTimeout(context.Background(), 5*time.Minute)
	defer cancel()

	clabDir := fmt.Sprintf("%s/%s", uc.clabDir, podID)
	clabFile := fmt.Sprintf("%s/clab.yml", clabDir)

	// Create directory and write topology YAML
	mkdirCmd := exec.CommandContext(ctx, "mkdir", "-p", clabDir)
	if err := mkdirCmd.Run(); err != nil {
		slog.Error("lab mkdir failed", slog.String("submission_id", submissionID.String()), slog.String("error", err.Error()))
		uc.labRepo.UpdateSubmissionStatus(context.Background(), submissionID, domain.LabStatusFailed, nil, 0)
		return
	}

	// Write the topology file
	writeFile := fmt.Sprintf("cat > %s << 'CLABEOF'\n%s\nCLABEOF", clabFile, lab.TopologyYAML)
	writeCmd := exec.CommandContext(ctx, "sh", "-c", writeFile)
	if err := writeCmd.Run(); err != nil {
		slog.Error("lab write clab.yml failed", slog.String("submission_id", submissionID.String()), slog.String("error", err.Error()))
		uc.labRepo.UpdateSubmissionStatus(context.Background(), submissionID, domain.LabStatusFailed, nil, 0)
		return
	}

	// Run containerlab deploy
	deployCmd := exec.CommandContext(ctx, uc.clabBinPath, "deploy", "-t", clabFile)
	output, err := deployCmd.CombinedOutput()
	if err != nil {
		slog.Error("lab containerlab deploy failed",
			slog.String("submission_id", submissionID.String()),
			slog.String("error", err.Error()),
			slog.String("output", string(output)))
		uc.labRepo.UpdateSubmissionStatus(context.Background(), submissionID, domain.LabStatusFailed, nil, 0)
		return
	}

	slog.Info("lab deployed successfully",
		slog.String("submission_id", submissionID.String()),
		slog.String("output", string(output)))

	// Parse device info from containerlab inspect
	devices := uc.parseDevicesFromDeploy(ctx, podID)

	// Update submission with device info
	uc.labRepo.UpdateSubmissionStatus(context.Background(), submissionID, domain.LabStatusRunning, devices, 0)
}

// parseDevicesFromDeploy runs `containerlab inspect` to get device details.
func (uc *LabUseCase) parseDevicesFromDeploy(ctx context.Context, podID string) []domain.LabDevice {
	// Use containerlab inspect to get device information
	inspectCmd := exec.CommandContext(ctx, uc.clabBinPath, "inspect", "-n", podID, "--format", "json")
	output, err := inspectCmd.CombinedOutput()
	if err != nil {
		slog.Error("failed to inspect lab",
			slog.String("pod_id", podID),
			slog.String("error", err.Error()),
			slog.String("output", string(output)))
		// Fallback: try docker ps to get running containers
		return uc.fallbackDevices(podID)
	}

	// Parse JSON output from containerlab inspect
	return uc.parseCLabJSON(string(output), podID)
}

func (uc *LabUseCase) parseCLabJSON(output, podID string) []domain.LabDevice {
	var devices []domain.LabDevice

	// Simple line-based parser for containerlab inspect JSON
	// Format: {"containers":{"clab-{pod}-{name}":{"name":"{name}","kind":"{kind}","mgmt_ip":"...",...}}}
	lines := strings.Split(output, "\n")
	currentName := ""
	for _, line := range lines {
		trimmed := strings.TrimSpace(line)
		if strings.Contains(trimmed, fmt.Sprintf(`"clab-%s-`, podID)) {
			// Extract device name from container name: "clab-{pod}-{name}"
			parts := strings.Split(trimmed, `"`)
			for _, p := range parts {
				if strings.Contains(p, fmt.Sprintf("clab-%s-", podID)) {
					nameParts := strings.Split(p, "-")
					if len(nameParts) > 3 {
						currentName = strings.Join(nameParts[3:], "-")
					}
				}
			}
		}
		if currentName != "" && strings.Contains(trimmed, `"mgmt_ip"`) {
			parts := strings.Split(trimmed, `"`)
			for i, p := range parts {
				if p == "mgmt_ip" && i+2 < len(parts) {
					ip := parts[i+2]
					devices = append(devices, domain.LabDevice{
						Name:   currentName,
						Kind:   "juniper_crpd",
						MgmtIP: ip,
						Status: domain.DeviceStatusRunning,
					})
					currentName = ""
					break
				}
			}
		}
	}

	if len(devices) == 0 {
		return uc.fallbackDevices(podID)
	}
	return devices
}

func (uc *LabUseCase) fallbackDevices(podID string) []domain.LabDevice {
	// Use docker ps to find containers belonging to this lab
	ctx, cancel := context.WithTimeout(context.Background(), 10*time.Second)
	defer cancel()

	cmd := exec.CommandContext(ctx, "docker", "ps", "--filter", fmt.Sprintf("name=clab-%s-", podID), "--format", "{{.Names}}")
	output, err := cmd.CombinedOutput()
	if err != nil {
		slog.Error("fallback devices failed", slog.String("pod_id", podID), slog.String("error", err.Error()))
		return nil
	}

	var devices []domain.LabDevice
	for _, name := range strings.Split(strings.TrimSpace(string(output)), "\n") {
		if name == "" {
			continue
		}
		parts := strings.Split(name, "-")
		deviceName := parts[len(parts)-1]
		devices = append(devices, domain.LabDevice{
			Name:   deviceName,
			Kind:   "juniper_crpd",
			Status: domain.DeviceStatusRunning,
		})
	}
	return devices
}

// StopLab stops a running lab session and cleans up Containerlab.
func (uc *LabUseCase) StopLab(ctx context.Context, userID uuid.UUID, submissionID uuid.UUID) error {
	sub, err := uc.labRepo.GetSubmission(ctx, submissionID)
	if err != nil {
		return fmt.Errorf("get submission: %w", err)
	}
	if sub == nil {
		return fmt.Errorf("submission not found")
	}
	if sub.UserID != userID {
		return fmt.Errorf("submission does not belong to user")
	}

	// Destroy Containerlab topology
	clabDir := fmt.Sprintf("%s/%s", uc.clabDir, sub.PodID)
	destroyCmd := exec.CommandContext(ctx, uc.clabBinPath, "destroy", "-t", fmt.Sprintf("%s/clab.yml", clabDir))
	if output, err := destroyCmd.CombinedOutput(); err != nil {
		slog.Warn("containerlab destroy failed",
			slog.String("pod_id", sub.PodID),
			slog.String("error", err.Error()),
			slog.String("output", string(output)))
		// Continue with cleanup anyway
	}

	// Clean up directory
	exec.CommandContext(ctx, "rm", "-rf", clabDir).Run()

	// Calculate final score
	totalScore := 0
	scores, err := uc.labRepo.GetLabScores(ctx, submissionID)
	if err == nil {
		for _, s := range scores {
			totalScore += s.TaskScore
		}
	}

	return uc.labRepo.CompleteSubmission(ctx, submissionID, domain.LabStatusCompleted, totalScore)
}

// PauseLab pauses a lab session (creates snapshot).
func (uc *LabUseCase) PauseLab(ctx context.Context, userID uuid.UUID, submissionID uuid.UUID) error {
	sub, err := uc.labRepo.GetSubmission(ctx, submissionID)
	if err != nil {
		return fmt.Errorf("get submission: %w", err)
	}
	if sub == nil || sub.UserID != userID {
		return fmt.Errorf("submission not found or access denied")
	}

	// Save container state (commit configs before pause)
	// In a real implementation, we'd use docker commit or containerlab save
	uc.labRepo.UpdateSubmissionStatus(ctx, submissionID, domain.LabStatusPaused, sub.Devices, sub.CurrentScore)
	return nil
}

// ResumeLab resumes a paused lab session.
func (uc *LabUseCase) ResumeLab(ctx context.Context, userID uuid.UUID, submissionID uuid.UUID) error {
	sub, err := uc.labRepo.GetSubmission(ctx, submissionID)
	if err != nil {
		return fmt.Errorf("get submission: %w", err)
	}
	if sub == nil || sub.UserID != userID {
		return fmt.Errorf("submission not found or access denied")
	}

	uc.labRepo.UpdateSubmissionStatus(ctx, submissionID, domain.LabStatusRunning, sub.Devices, sub.CurrentScore)
	return nil
}

// SubmitModule grades a specific module of the lab by running the lab's
// grade.py script via docker exec inside the Containerlab DinD container.
func (uc *LabUseCase) SubmitModule(ctx context.Context, userID uuid.UUID, req *domain.LabSubmitModuleRequest) (*domain.LabScore, error) {
	sub, err := uc.labRepo.GetSubmission(ctx, req.SubmissionID)
	if err != nil {
		return nil, fmt.Errorf("get submission: %w", err)
	}
	if sub == nil || sub.UserID != userID {
		return nil, fmt.Errorf("submission not found or access denied")
	}

	// Load the lab template to get grading script path
	lab, err := uc.labRepo.GetByID(ctx, sub.LabID)
	if err != nil {
		return nil, fmt.Errorf("get lab: %w", err)
	}
	if lab == nil {
		return nil, fmt.Errorf("lab not found")
	}

	// Build device IP arguments from submission's devices
	// Map device names to their management IPs
	// grade.py expects flags like: --r1-ip <ip> --r2-ip <ip> --r3-ip <ip>
	var deviceArgs []string
	for _, dev := range sub.Devices {
		if dev.MgmtIP != "" {
			deviceArgs = append(deviceArgs, fmt.Sprintf("--%s-ip", dev.Name), dev.MgmtIP)
		}
	}

	// Determine the grading script path on disk
	if lab.GradingScript == "" {
		return nil, fmt.Errorf("lab has no grading script configured")
	}
	if lab.LabDirectory == "" {
		return nil, fmt.Errorf("lab has no lab_directory configured")
	}

	// Path construction:
	//   lab_directory = "backend/labs/micro-labs/01-junos-cli-basics"
	//   labsBaseDir   = "/app/labs" (mounted from ../backend/labs)
	//   GradingScript = "01-junos-cli-basics/grade.py"
	//   → /app/labs/micro-labs/01-junos-cli-basics/grade.py
	//
	// Strip the "backend/labs/" prefix from lab_directory to get the
	// path relative to labsBaseDir, then append the grade.py filename.
	relDir := strings.TrimPrefix(lab.LabDirectory, "backend/labs/")
	gradeScriptPath := filepath.Join(uc.labsBaseDir, relDir, filepath.Base(lab.GradingScript))

	// Run the grading script inside the DinD container via the host Docker socket
	var gradeOutput []byte
	gradeOutput, err = uc.runGradeScript(ctx, gradeScriptPath, deviceArgs)
	if err != nil {
		slog.Error("SubmitModule: grade.py execution failed", slog.String("error", err.Error()))
		// Fallback: return a zero score with error info
		return uc.saveZeroScore(ctx, sub, req, fmt.Sprintf("grading error: %v", err))
	}

	// Parse the JSON output from grade.py
	var pyResult domain.PythonGradeOutput
	if err := json.Unmarshal(gradeOutput, &pyResult); err != nil {
		slog.Error("SubmitModule: failed to parse grade.py JSON",
			slog.String("error", err.Error()),
			slog.String("raw", string(gradeOutput)))
		return uc.saveZeroScore(ctx, sub, req, fmt.Sprintf("parse error: %v", err))
	}

	// Convert Python grading tasks to ScoringCheck array
	scoringChecks := make([]domain.ScoringCheck, 0, len(pyResult.Tasks))
	for taskID, task := range pyResult.Tasks {
		scoringChecks = append(scoringChecks, domain.ScoringCheck{
			Command:       taskID,
			ExpectedMatch: "",
			ActualOutput:  task.Detail,
			Passed:        task.Passed,
			PointsAwarded: task.Score,
			MaxPoints:     task.MaxScore,
		})
	}

	// Build LabScore from grade result
	score := &domain.LabScore{
		ID:            uuid.New(),
		SubmissionID:  req.SubmissionID,
		ModuleNumber:  req.ModuleNumber,
		ModuleTitle:   pyResult.Title,
		TaskScore:     pyResult.TotalScore,
		MaxScore:      pyResult.MaxScore,
		ScoringOutput: scoringChecks,
		IsAutoGraded:  true,
		CreatedAt:     time.Now().UTC(),
	}

	if err := uc.labRepo.SaveLabScore(ctx, score); err != nil {
		return nil, fmt.Errorf("save score: %w", err)
	}

	// Update submission current_score
	scores, _ := uc.labRepo.GetLabScores(ctx, req.SubmissionID)
	total := 0
	for _, s := range scores {
		total += s.TaskScore
	}
	uc.labRepo.UpdateSubmissionStatus(ctx, req.SubmissionID, sub.Status, sub.Devices, total)

	return score, nil
}

// runGradeScript reads a grade.py script and executes it inside the DinD container
// via the host Docker socket. The grade.py script connects to lab devices via SSH
// using their management IPs (only reachable from inside the DinD container).
func (uc *LabUseCase) runGradeScript(ctx context.Context, scriptPath string, extraArgs []string) ([]byte, error) {
	// Read the Python script content from disk
	scriptBytes, err := os.ReadFile(scriptPath)
	if err != nil {
		return nil, fmt.Errorf("read grade script %s: %w", scriptPath, err)
	}

	// Build docker exec command to run the script inside DinD
	// Use the host Docker socket (not DOCKER_HOST pointing to DinD) so we can
	// exec into the clab-dind container itself (not from inside DinD's Docker)
	// The -H flag overrides DOCKER_HOST for this specific command.
	args := []string{
		"-H", fmt.Sprintf("unix://%s", uc.hostDockerSocket),
		"exec", "-i", uc.dindContainer,
		"python3", "-",
		"--output", "json",
	}
	args = append(args, extraArgs...)

	cmd := exec.CommandContext(ctx, "docker", args...)
	cmd.Stdin = bytes.NewReader(scriptBytes)

	output, err := cmd.CombinedOutput()
	if err != nil {
		// If the command failed, include the output in the error for debugging
		return nil, fmt.Errorf("docker exec failed: %w\nOutput: %s", err, string(output))
	}

	// Strip any non-JSON prefix (e.g., warnings printed to stdout before JSON)
	outStr := strings.TrimSpace(string(output))
	jsonStart := strings.Index(outStr, "{")
	if jsonStart > 0 {
		outStr = outStr[jsonStart:]
	}

	return []byte(outStr), nil
}

// saveZeroScore creates a placeholder LabScore with 0 points and an error detail.
func (uc *LabUseCase) saveZeroScore(ctx context.Context, sub *domain.LabSubmission, req *domain.LabSubmitModuleRequest, errDetail string) (*domain.LabScore, error) {
	score := &domain.LabScore{
		ID:           uuid.New(),
		SubmissionID: req.SubmissionID,
		ModuleNumber: req.ModuleNumber,
		ModuleTitle:  fmt.Sprintf("Module %d", req.ModuleNumber),
		TaskScore:    0,
		MaxScore:     100,
		ScoringOutput: []domain.ScoringCheck{
			{Command: "error", ActualOutput: errDetail, Passed: false, PointsAwarded: 0, MaxPoints: 100},
		},
		IsAutoGraded: true,
		CreatedAt:    time.Now().UTC(),
	}

	if err := uc.labRepo.SaveLabScore(ctx, score); err != nil {
		return nil, fmt.Errorf("save fallback score: %w", err)
	}

	scores, _ := uc.labRepo.GetLabScores(ctx, req.SubmissionID)
	total := 0
	for _, s := range scores {
		total += s.TaskScore
	}
	uc.labRepo.UpdateSubmissionStatus(ctx, req.SubmissionID, sub.Status, sub.Devices, total)

	return score, nil
}

// GetSubmission returns a lab submission by ID.
// Ownership is enforced: userID must match submission.UserID, otherwise
// domain.ErrForbidden is returned (IDOR protection — see AUDIT_TECHNICAL.md §1.1).
func (uc *LabUseCase) GetSubmission(ctx context.Context, userID, id uuid.UUID) (*domain.LabSubmission, error) {
	sub, err := uc.labRepo.GetSubmission(ctx, id)
	if err != nil {
		return nil, err
	}
	if sub == nil {
		return nil, domain.ErrNotFound
	}
	if sub.UserID != userID {
		return nil, domain.ErrForbidden
	}
	return sub, nil
}

// GetScores returns all scores for a submission.
// Ownership is enforced: userID must match the submission owner, otherwise
// domain.ErrForbidden is returned (IDOR protection — see AUDIT_TECHNICAL.md §1.1).
func (uc *LabUseCase) GetScores(ctx context.Context, userID, submissionID uuid.UUID) ([]domain.LabScore, error) {
	sub, err := uc.labRepo.GetSubmission(ctx, submissionID)
	if err != nil {
		return nil, err
	}
	if sub == nil {
		return nil, domain.ErrNotFound
	}
	if sub.UserID != userID {
		return nil, domain.ErrForbidden
	}
	return uc.labRepo.GetLabScores(ctx, submissionID)
}

// GetActiveSubmissions returns active submissions for a user.
func (uc *LabUseCase) GetActiveSubmissions(ctx context.Context, userID uuid.UUID) ([]domain.LabSubmission, error) {
	return uc.labRepo.GetActiveSubmissionsByUser(ctx, userID)
}

// GetWebSocketURL returns the WebSocket URL for terminal connections.
func (uc *LabUseCase) GetWebSocketURL(submissionID uuid.UUID, deviceName string) string {
	return fmt.Sprintf("ws://%s:%s/ws/lab/%s/%s", uc.wsHost, uc.wsPort, submissionID.String(), deviceName)
}
