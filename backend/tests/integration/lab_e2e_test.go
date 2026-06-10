//go:build integration

// Package integration_test contains end-to-end tests that run against the
// real staging stack (clab-dind with Containerlab + Python3).
//
// Prerequisites:
//   - Docker is installed and the current user has Docker access.
//   - The staging stack is up: docker compose -f infra/docker-compose.staging.yml up -d
//   - clab-dind is healthy with containerlab v0.75.0+ and Python 3.12+
//
// Run:
//   cd backend && go test -tags=integration -v ./tests/integration/ -timeout 300s
package integration_test

import (
	"encoding/json"
	"fmt"
	"os"
	"os/exec"
	"path/filepath"
	"strings"
	"testing"
	"time"
)

// Environment variables for test configuration.
const (
	envDindContainer  = "DIND_CONTAINER"   // clab-dind container name (default: netcert-staging-clab-dind)
	envLabsMountDir   = "LABS_MOUNT_DIR"   // labs mount path inside DinD (default: /labs)
	envSkipCleanup    = "TEST_SKIP_CLEANUP" // set to "true" to preserve lab after test for debugging
	envClabNamePrefix = "CLAB_NAME_PREFIX" // prefix for test topology name (default: netcert-test-)
)

// GradingTask represents a single task result from grade.py JSON output.
type GradingTask struct {
	Score    int    `json:"score"`
	MaxScore int    `json:"max_score"`
	Passed   bool   `json:"passed"`
	Detail   string `json:"detail"`
}

// GradingResult represents the full JSON output from grade.py.
type GradingResult struct {
	Lab        string                `json:"lab"`
	Title      string                `json:"title"`
	Level      string                `json:"level"`
	MaxScore   int                   `json:"max_score"`
	TotalScore int                   `json:"total_score"`
	Passed     bool                  `json:"passed"`
	Tasks      map[string]GradingTask `json:"tasks"`
}

// testConfig holds all configuration derived from env + defaults.
type testConfig struct {
	dindContainer string
	labsMountDir  string
	skipCleanup   bool
	clabPrefix    string
}

func loadConfig() testConfig {
	cfg := testConfig{
		dindContainer: "netcert-staging-clab-dind",
		labsMountDir:  "/labs",
		clabPrefix:    "netcert-test-",
	}
	if v := os.Getenv(envDindContainer); v != "" {
		cfg.dindContainer = v
	}
	if v := os.Getenv(envLabsMountDir); v != "" {
		cfg.labsMountDir = v
	}
	if v := os.Getenv(envSkipCleanup); v == "true" || v == "1" {
		cfg.skipCleanup = true
	}
	if v := os.Getenv(envClabNamePrefix); v != "" {
		cfg.clabPrefix = v
	}
	return cfg
}

// =============================================================================
// Helpers: run Docker commands inside clab-dind
// =============================================================================

// dockerExec runs a command inside the clab-dind container and returns
// combined stdout+stderr.
func dockerExec(t *testing.T, cfg testConfig, workDir string, args ...string) (string, error) {
	t.Helper()
	dockerArgs := []string{"exec", "-i"}
	if workDir != "" {
		dockerArgs = append(dockerArgs, "-w", workDir)
	}
	dockerArgs = append(dockerArgs, cfg.dindContainer)
	dockerArgs = append(dockerArgs, args...)

	cmd := exec.Command("docker", dockerArgs...)
	out, err := cmd.CombinedOutput()
	return strings.TrimSpace(string(out)), err
}

// dockerExecPipe runs a command inside clab-dind with stdin piped from
// pipeContent and returns combined stdout+stderr.
func dockerExecPipe(t *testing.T, cfg testConfig, pipeContent string, args ...string) (string, error) {
	t.Helper()
	dockerArgs := []string{"exec", "-i", cfg.dindContainer}
	dockerArgs = append(dockerArgs, args...)

	cmd := exec.Command("docker", dockerArgs...)
	cmd.Stdin = strings.NewReader(pipeContent)
	out, err := cmd.CombinedOutput()
	return strings.TrimSpace(string(out)), err
}

// dockerCopy copies a local file into the DinD container at the given path.
func dockerCopy(t *testing.T, cfg testConfig, localPath, remotePath string) error {
	t.Helper()
	cmd := exec.Command("docker", "cp", localPath, cfg.dindContainer+":"+remotePath)
	out, err := cmd.CombinedOutput()
	if err != nil {
		return fmt.Errorf("docker cp failed: %v\nOutput: %s", err, string(out))
	}
	return nil
}

// dockerExecMulti runs multiple commands in a single shell session inside DinD.
func dockerExecMulti(t *testing.T, cfg testConfig, workDir string, script string) (string, error) {
	t.Helper()
	return dockerExec(t, cfg, workDir, "sh", "-c", script)
}

// =============================================================================
// Prerequisites check
// =============================================================================

// checkPrerequisites verifies Docker access and clab-dind health.
func checkPrerequisites(t *testing.T, cfg testConfig) {
	t.Helper()

	// 1. Docker available
	cmd := exec.Command("docker", "version", "--format", "{{.Server.Version}}")
	out, err := cmd.CombinedOutput()
	if err != nil {
		t.Skipf("Docker not available: %v\nOutput: %s", err, string(out))
	}

	// 2. clab-dind container running
	cmd = exec.Command("docker", "ps", "--filter", fmt.Sprintf("name=%s", cfg.dindContainer),
		"--format", "{{.Names}}")
	out, err = cmd.CombinedOutput()
	if err != nil || !strings.Contains(string(out), cfg.dindContainer) {
		t.Skipf("DinD container %s not running. Start staging stack first:\n"+
			"  docker compose -f infra/docker-compose.staging.yml up -d\n%s",
			cfg.dindContainer, string(out))
	}

	// 3. Containerlab available inside DinD
	verOut, err := dockerExec(t, cfg, "", "containerlab", "version")
	if err != nil {
		t.Skipf("containerlab not found in %s: %v\n%s", cfg.dindContainer, err, verOut)
	}
	if !strings.Contains(verOut, "version") {
		t.Skipf("containerlab version check unexpected output: %s", verOut)
	}
	t.Logf("Containerlab: %s", strings.SplitN(verOut, "\n", 2)[0])

	// 4. Python 3 available
	pyVer, err := dockerExec(t, cfg, "", "python3", "--version")
	if err != nil {
		t.Skipf("python3 not found in %s: %v", cfg.dindContainer, err)
	}
	t.Logf("Python: %s", pyVer)

	// 5. paramiko available
	paramikoOut, err := dockerExec(t, cfg, "", "python3", "-c",
		"import paramiko; print(paramiko.__version__)")
	if err != nil {
		t.Skipf("paramiko not available in %s: %v", cfg.dindContainer, err)
	}
	t.Logf("paramiko: %s", paramikoOut)

	// 6. cRPD image available
	// First try to pull; if that fails, check what's cached.
	pullOut, _ := dockerExec(t, cfg, "", "docker", "pull", "crpd:24.2R1")
	t.Logf("cRPD pull result: %s", truncate(pullOut, 120))

	imagesOut, err := dockerExec(t, cfg, "", "docker", "images",
		"--format", "{{.Repository}}:{{.Tag}}")
	if err != nil {
		t.Skipf("Failed to list Docker images in %s: %v", cfg.dindContainer, err)
	}
	t.Logf("Docker images in DinD:\n%s", imagesOut)

	if !strings.Contains(imagesOut, "crpd:24.2R1") {
		t.Skipf("cRPD image crpd:24.2R1 not available in %s.\n"+
			"This test requires the Juniper cRPD image (licensed). To proceed:\n"+
			"  1. Download crpd-24.2R1.tgz from Juniper Support Portal\n"+
			"  2. docker exec %s docker load -i /path/to/crpd-24.2R1.tgz\n"+
			"  Or use a different cRPD version and update the clab.yml files.",
			cfg.dindContainer, cfg.dindContainer)
	}
	t.Logf("cRPD image: available")

	// 7. Labs directory mounted
	lsOut, err := dockerExec(t, cfg, "", "ls", cfg.labsMountDir+"/micro-labs/01-junos-cli-basics/grade.py")
	if err != nil {
		t.Skipf("Labs directory not mounted at %s: %v", cfg.labsMountDir, err)
	}
	t.Logf("Labs mount: OK (%s)", lsOut)
}

// =============================================================================
// Test: Micro-Lab End-to-End
// =============================================================================

// TestMicroLabE2E deploys a Containerlab topology inside the real DinD,
// verifies device connectivity via docker exec (simulating WebSocket terminal),
// and runs grade.py to validate auto-grading.
func TestMicroLabE2E(t *testing.T) {
	cfg := loadConfig()
	checkPrerequisites(t, cfg)

	// Generate a unique test name to avoid collisions with concurrent runs.
	testSuffix := fmt.Sprintf("e2e-%d", time.Now().UnixNano())
	labSlug := "junos-cli-basics"
	testClabName := cfg.clabPrefix + testSuffix
	labRelDir := "micro-labs/" + labSlug // relative to labs mount
	labFullDir := filepath.Join(cfg.labsMountDir, labRelDir)

	// Derive device mgmt IPs from the original topology.
	// Micro-Lab 01: r1=172.100.1.2, r2=172.100.1.3
	// We remap them to avoid conflicts with any running lab.
	mgmtR1 := "172.100.2.2"
	mgmtR2 := "172.100.2.3"

	// Temp directory inside DinD for the modified topology.
	testWorkDir := fmt.Sprintf("/tmp/%s", testClabName)
	t.Logf("Test lab: %s (work dir: %s)", testClabName, testWorkDir)
	t.Logf("Devices: r1=%s, r2=%s", mgmtR1, mgmtR2)

	// ---- Step 1: Prepare modified topology ----

	// Read the original clab.yml from the labs mount.
	origTopology, err := dockerExec(t, cfg, "", "cat",
		filepath.Join(labFullDir, "clab.yml"))
	if err != nil {
		t.Fatalf("Failed to read original clab.yml: %v\n%s", err, origTopology)
	}

	// Patch the topology:
	//   - Change lab name to the unique test name
	//   - Change mgmt-ipv4 addresses to our test range
	//   - Use absolute paths for binds (since we'll be in a different work dir)
	patched := strings.ReplaceAll(origTopology, "name: netcert-ml01-cli-basics",
		"name: "+testClabName)
	patched = strings.ReplaceAll(patched, "mgmt-ipv4: 172.100.1.2",
		"mgmt-ipv4: "+mgmtR1)
	patched = strings.ReplaceAll(patched, "mgmt-ipv4: 172.100.1.3",
		"mgmt-ipv4: "+mgmtR2)

	// Convert relative config paths to absolute inside DinD.
	patched = strings.ReplaceAll(patched,
		"configs/r1.cfg:/config/juniper.conf.gz:ro",
		labFullDir+"/configs/r1.cfg:/config/juniper.conf.gz:ro")
	patched = strings.ReplaceAll(patched,
		"configs/r2.cfg:/config/juniper.conf.gz:ro",
		labFullDir+"/configs/r2.cfg:/config/juniper.conf.gz:ro")

	t.Logf("Patched topology:\n%s", patched)

	// Create work directory inside DinD.
	_, err = dockerExecMulti(t, cfg, "", "mkdir -p "+testWorkDir)
	if err != nil {
		t.Fatalf("Failed to create work dir in DinD: %v", err)
	}
	defer func() {
		if !cfg.skipCleanup {
			dockerExecMulti(t, cfg, "",
				fmt.Sprintf("rm -rf %s", testWorkDir))
		}
	}()

	// Write patched topology to a temp file and copy into DinD.
	localTopo := filepath.Join(t.TempDir(), testClabName+"-clab.yml")
	if err := os.WriteFile(localTopo, []byte(patched), 0644); err != nil {
		t.Fatalf("Failed to write patched topology: %v", err)
	}
	if err := dockerCopy(t, cfg, localTopo,
		filepath.Join(testWorkDir, "clab.yml")); err != nil {
		t.Fatalf("Failed to copy topology into DinD: %v", err)
	}

	// ---- Step 2: Deploy topology ----

	t.Log("Deploying Containerlab topology...")
	clabFile := filepath.Join(testWorkDir, "clab.yml")
	deployOut, err := dockerExec(t, cfg, testWorkDir,
		"containerlab", "deploy", "--reconfigure", "-t", clabFile)
	if err != nil {
		t.Fatalf("Containerlab deploy failed: %v\nOutput:\n%s", err, deployOut)
	}
	t.Logf("Deploy output:\n%s", deployOut)

	// Cleanup: destroy the lab when test finishes (or skip if TEST_SKIP_CLEANUP).
	defer func() {
		if cfg.skipCleanup {
			t.Logf("SKIP_CLEANUP=true — lab %s left running for debugging", testClabName)
			t.Logf("Destroy manually: docker exec %s containerlab destroy -t %s",
				cfg.dindContainer, clabFile)
			return
		}
		t.Log("Destroying Containerlab topology...")
		destroyOut, err := dockerExec(t, cfg, testWorkDir,
			"containerlab", "destroy", "-t", clabFile, "--cleanup")
		if err != nil {
			t.Logf("Warning: containerlab destroy failed: %v\nOutput: %s", err, destroyOut)
		} else {
			t.Logf("Destroyed: %s", destroyOut)
		}
	}()

	// ---- Step 3: Wait for devices to be ready ----

	t.Log("Waiting for devices to become ready...")
	r1Ready := waitForDevice(t, cfg, testClabName, "r1", 60*time.Second)
	r2Ready := waitForDevice(t, cfg, testClabName, "r2", 60*time.Second)

	if !r1Ready {
		t.Fatal("R1 did not become ready within timeout")
	}
	if !r2Ready {
		t.Fatal("R2 did not become ready within timeout")
	}
	t.Log("Both devices are ready.")

	// ---- Step 4: Test terminal access via docker exec ----

	// Give SSH a moment to be fully ready on both devices (grade.py uses
	// paramiko SSH, which may lag behind docker exec cli readiness).
	t.Log("Waiting for SSH to be ready on devices...")
	time.Sleep(8 * time.Second)

	t.Run("TerminalAccess", func(t *testing.T) {
		testTerminal(t, cfg, testClabName, "r1")
	})

	t.Run("DeviceConnectivity", func(t *testing.T) {
		testDeviceConnectivity(t, cfg, testClabName)
	})

	// ---- Step 5: Run grade.py Auto-Grading ----

	t.Run("AutoGrading", func(t *testing.T) {
		testAutoGrading(t, cfg, labFullDir, mgmtR1, mgmtR2)
	})
}

// =============================================================================
// Step 3 helper: wait for device readiness
// =============================================================================

// waitForDevice polls docker exec `cli` until the device responds or timeout.
func waitForDevice(t *testing.T, cfg testConfig, clabName, device string, timeout time.Duration) bool {
	t.Helper()
	containerName := fmt.Sprintf("clab-%s-%s", clabName, device)
	deadline := time.Now().Add(timeout)

	for time.Now().Before(deadline) {
		// Try: docker exec -i container cli -c "show version | match Model" 2>/dev/null
		out, err := dockerExecPipe(t, cfg, "",
			"docker", "exec", "-i", containerName,
			"cli", "-c", "show version | no-more")
		if err == nil && len(out) > 10 {
			t.Logf("Device %s ready: %s", device, truncate(out, 80))
			return true
		}
		time.Sleep(3 * time.Second)
	}
	// Last attempt with full error output
	out, err := dockerExec(t, cfg, "",
		"docker", "exec", "-i", containerName,
		"cli", "-c", "show version | no-more")
	t.Logf("Device %s last attempt: err=%v, out=%s", device, err, truncate(out, 200))
	return false
}

// =============================================================================
// Step 4: Terminal access (simulates WebSocket ↔ docker exec bridge)
// =============================================================================

// testTerminal verifies that we can execute JunOS CLI commands on a device
// via docker exec — the same mechanism the WebSocket SSH proxy uses internally.
func testTerminal(t *testing.T, cfg testConfig, clabName, device string) {
	containerName := fmt.Sprintf("clab-%s-%s", clabName, device)

	tests := []struct {
		name      string
		command   string
		check     func(string) bool
	}{
		{
			name:    "OperationalMode",
			command: "show version | no-more",
			check:   func(out string) bool { return strings.Contains(out, "JunOS") || strings.Contains(out, "junos") || strings.Contains(out, "JUNOS") },
		},
		{
			name:    "InterfacesTerse",
			command: "show interfaces terse | no-more",
			check:   func(out string) bool { return strings.Contains(out, "ge-0/0/0") && strings.Contains(out, "lo0") },
		},
		{
			name:    "ConfigurationMode",
			command: "show configuration system host-name | no-more",
			check:   func(out string) bool { return len(out) > 5 },
		},
	}

	for _, tt := range tests {
		t.Run(tt.name, func(t *testing.T) {
			out, err := dockerExecPipe(t, cfg, "",
				"docker", "exec", "-i", containerName,
				"cli", "-c", tt.command)
			if err != nil {
				t.Fatalf("Command %q failed: %v\nOutput: %s", tt.command, err, truncate(out, 300))
			}
			if !tt.check(out) {
				t.Errorf("Command %q output check failed.\nExpected condition not met.\nOutput:\n%s",
					tt.command, truncate(out, 500))
			} else {
				t.Logf("✓ %s: %s", tt.name, truncate(out, 80))
			}
		})
	}
}

// testDeviceConnectivity verifies that devices can reach each other.
func testDeviceConnectivity(t *testing.T, cfg testConfig, clabName string) {
	r1Container := fmt.Sprintf("clab-%s-%s", clabName, "r1")

	// Ping from R1 to R2 (10.0.12.2) — this should work since devices
	// are directly connected via ge-0/0/0.
	t.Run("PingR1toR2", func(t *testing.T) {
		out, err := dockerExecPipe(t, cfg, "",
			"docker", "exec", "-i", r1Container,
			"cli", "-c", "ping 10.0.12.2 count 3 rapid | no-more")
		if err != nil {
			t.Fatalf("Ping failed: %v\nOutput: %s", err, truncate(out, 300))
		}
		if strings.Contains(out, "packets received") && !strings.Contains(out, "0 packets received") {
			t.Logf("✓ Ping R1→R2 successful: %s", truncate(out, 80))
		} else {
			t.Errorf("Ping R1→R2 may have failed. Output:\n%s", truncate(out, 300))
		}
	})

	// Show LLDP neighbors
	t.Run("LLDPNeighbors", func(t *testing.T) {
		out, err := dockerExecPipe(t, cfg, "",
			"docker", "exec", "-i", r1Container,
			"cli", "-c", "show lldp neighbors | no-more")
		if err != nil {
			t.Logf("LLDP not available (expected for cRPD): %v", err)
		} else {
			t.Logf("LLDP output: %s", truncate(out, 200))
		}
	})
}

// =============================================================================
// Step 5: Auto-Grading via grade.py
// =============================================================================

// testAutoGrading runs grade.py against the deployed lab devices and
// verifies the JSON scoring output is well-formed.
func testAutoGrading(t *testing.T, cfg testConfig, labFullDir, r1IP, r2IP string) {
	// Read the grade.py script.
	gradeScript, err := dockerExec(t, cfg, "", "cat",
		filepath.Join(labFullDir, "grade.py"))
	if err != nil {
		t.Fatalf("Failed to read grade.py: %v\n%s", err, gradeScript)
	}

	// Run grade.py via the pipe mechanism (same as LabUseCase.runGradeScript).
	// Pipe the script through stdin to python3 - inside DinD.
	t.Logf("Running grade.py against r1=%s, r2=%s...", r1IP, r2IP)
	out, err := dockerExecPipe(t, cfg, gradeScript,
		"python3", "-",
		"--r1-ip", r1IP,
		"--r2-ip", r2IP,
		"--output", "json")
	if err != nil {
		t.Fatalf("grade.py execution failed: %v\nOutput:\n%s", err, out)
	}

	t.Logf("Grade output:\n%s", truncate(out, 1000))

	// Parse JSON output.
	var result GradingResult
	if err := json.Unmarshal([]byte(out), &result); err != nil {
		// The script might output warnings before JSON; try to extract JSON.
		if idx := strings.Index(out, "{"); idx >= 0 {
			cleaned := out[idx:]
			if err2 := json.Unmarshal([]byte(cleaned), &result); err2 != nil {
				t.Fatalf("Failed to parse grade.py JSON output (tried raw and sliced):\n"+
					"raw error: %v\nsliced error: %v\nRaw output:\n%s", err, err2, out)
			}
		} else {
			t.Fatalf("Failed to parse grade.py JSON output: %v\nRaw output:\n%s", err, out)
		}
	}

	// Validate result structure.
	if result.Lab == "" {
		t.Error("grade.py result missing 'lab' field")
	}
	if result.Title == "" {
		t.Error("grade.py result missing 'title' field")
	}
	if result.MaxScore <= 0 {
		t.Errorf("grade.py max_score should be >0, got %d", result.MaxScore)
	}
	if len(result.Tasks) == 0 {
		t.Error("grade.py result has no tasks")
	}

	// Log each task result.
	for taskID, task := range result.Tasks {
		status := "✓" 
		if !task.Passed {
			status = "✗"
		}
		t.Logf("  %s %s: %d/%d — %s", status, taskID, task.Score, task.MaxScore,
			truncate(task.Detail, 100))
	}

	t.Logf("Total score: %d/%d (passed=%v)", result.TotalScore, result.MaxScore, result.Passed)

	// Basic check: total score should be between 0 and max_score.
	if result.TotalScore < 0 || result.TotalScore > result.MaxScore {
		t.Errorf("total_score=%d out of range [0, %d]", result.TotalScore, result.MaxScore)
	}

	// Check task scores are internally consistent.
	for taskID, task := range result.Tasks {
		if task.Score < 0 || task.Score > task.MaxScore {
			t.Errorf("task %s: score=%d out of range [0, %d]", taskID, task.Score, task.MaxScore)
		}
		if task.MaxScore <= 0 {
			t.Errorf("task %s: max_score=%d should be >0", taskID, task.MaxScore)
		}
	}

	// Since this is a clean topology with initial configs (no student changes),
	// specific tasks will pass and others won't.
	// The important thing is the JSON structure is valid and tools parse it.
	t.Log("✓ grade.py JSON structure is valid and parseable")

	// Verify the output matches the PythonGradeOutput domain struct.
	// Task "task1_explore" should pass because interfaces are already configured.
	verifyExpectedTask(t, result.Tasks, "task1_explore", 0, 15)
}

// verifyExpectedTask checks that a specific task has expected max_score.
func verifyExpectedTask(t *testing.T, tasks map[string]GradingTask, taskID string, minScore, maxScore int) {
	t.Helper()
	task, ok := tasks[taskID]
	if !ok {
		t.Logf("Note: task %q not found in grade.py output (expected for fresh deploy)", taskID)
		return
	}
	if task.MaxScore != maxScore {
		t.Errorf("task %s max_score=%d, expected %d", taskID, task.MaxScore, maxScore)
	}
	if task.Score < minScore || task.Score > maxScore {
		t.Errorf("task %s score=%d out of expected range [%d, %d]",
			taskID, task.Score, minScore, maxScore)
	}
}

// =============================================================================
// Utilities
// =============================================================================

// truncate truncates a string to maxLen and adds "…" if needed.
func truncate(s string, maxLen int) string {
	runes := []rune(s)
	if len(runes) <= maxLen {
		return s
	}
	return string(runes[:maxLen]) + "…"
}
