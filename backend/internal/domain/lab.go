package domain

import (
	"time"

	"github.com/google/uuid"
)

type LabStatus string

const (
	LabStatusPending    LabStatus = "pending"
	LabStatusDeploying  LabStatus = "deploying"
	LabStatusRunning    LabStatus = "running"
	LabStatusPaused     LabStatus = "paused"
	LabStatusCompleted  LabStatus = "completed"
	LabStatusFailed     LabStatus = "failed"
	LabStatusTimedOut   LabStatus = "timed_out"
)

type DeviceStatus string

const (
	DeviceStatusStarting  DeviceStatus = "starting"
	DeviceStatusRunning   DeviceStatus = "running"
	DeviceStatusStopped   DeviceStatus = "stopped"
	DeviceStatusError     DeviceStatus = "error"
)

// Lab represents a lab template (defined in the system).
type Lab struct {
	ID              uuid.UUID              `json:"id"`
	TrackID         uuid.UUID              `json:"track_id"`
	Slug            string                 `json:"slug"`
	Title           string                 `json:"title"`
	Description     string                 `json:"description"`
	Level           Level                  `json:"level"`
	DurationMinutes int                    `json:"duration_minutes"`
	TopologyYAML    string                 `json:"topology_yaml,omitempty"`
	InitialConfigs  map[string]string      `json:"initial_configs,omitempty"`
	TaskDescription string                 `json:"task_description"`
	GradingScript   string                 `json:"grading_script,omitempty"`
	FaultConfig     map[string]interface{} `json:"fault_config,omitempty"`
	IsTroubleshooting bool                `json:"is_troubleshooting"`
	Technology      string                 `json:"technology"`
	MaxScore        int                    `json:"max_score"`
	PassingScore    int                    `json:"passing_score"`
	NumDevices      int                    `json:"num_devices"`
	LabDirectory    string                 `json:"lab_directory"`
	IsActive        bool                   `json:"is_active"`
	CreatedAt       time.Time              `json:"created_at"`
	UpdatedAt       time.Time              `json:"updated_at"`
}

// LabDevice represents a device inside a running lab session.
type LabDevice struct {
	Name       string       `json:"name"`
	Kind       string       `json:"kind"`
	MgmtIP     string       `json:"mgmt_ip"`
	SSHPort    int          `json:"ssh_port"`
	Status     DeviceStatus `json:"status"`
	Interfaces []DeviceInterface `json:"interfaces,omitempty"`
}

type DeviceInterface struct {
	ID       string `json:"id"`
	Status   string `json:"status"`
	Neighbor string `json:"neighbor,omitempty"`
	IP       string `json:"ip,omitempty"`
}

// LabSubmission represents a user's lab session.
type LabSubmission struct {
	ID                 uuid.UUID   `json:"id"`
	LabID              uuid.UUID   `json:"lab_id"`
	UserID             uuid.UUID   `json:"user_id"`
	Status             LabStatus   `json:"status"`
	PodID              string      `json:"pod_id"`
	Devices            []LabDevice `json:"devices,omitempty"`
	StartedAt          time.Time   `json:"started_at"`
	CompletedAt        *time.Time  `json:"completed_at,omitempty"`
	TimeRemainingSec   int         `json:"time_remaining_seconds"`
	CurrentScore       int         `json:"current_score"`
	MaxScore           int         `json:"max_score"`
	SnapshotID         *string     `json:"snapshot_id,omitempty"`
	TopologyUpdateURL  string      `json:"topology_update_url,omitempty"`
	TerminalWSURL      string      `json:"terminal_ws_url,omitempty"`
	CreatedAt          time.Time   `json:"created_at"`
}

// LabScore represents grading results for a lab module.
type LabScore struct {
	ID             uuid.UUID              `json:"id"`
	SubmissionID   uuid.UUID              `json:"submission_id"`
	ModuleNumber   int                    `json:"module_number"`
	ModuleTitle    string                 `json:"module_title"`
	TaskScore      int                    `json:"task_score"`
	MaxScore       int                    `json:"max_score"`
	ScoringOutput  []ScoringCheck         `json:"scoring_output,omitempty"`
	IsAutoGraded   bool                   `json:"is_autograded"`
	CreatedAt      time.Time              `json:"created_at"`
}

type ScoringCheck struct {
	Command        string `json:"command"`
	ExpectedMatch  string `json:"expected_match"`
	ActualOutput   string `json:"actual_output"`
	Passed         bool   `json:"passed"`
	PointsAwarded  int    `json:"points_awarded"`
	MaxPoints      int    `json:"max_points"`
}

// LabStartRequest is the request to start a lab session.
type LabStartRequest struct {
	LabID  uuid.UUID `json:"lab_id"`
	Mode   string    `json:"mode"` // "exam", "practice", "free_play"
}

// PythonGradeOutput represents the JSON output from a grade.py grading script.
type PythonGradeOutput struct {
	Lab        string                       `json:"lab"`
	Title      string                       `json:"title"`
	Level      string                       `json:"level"`
	MaxScore   int                          `json:"max_score"`
	TotalScore int                          `json:"total_score"`
	Passed     bool                         `json:"passed"`
	Tasks      map[string]PythonGradeTask   `json:"tasks"`
}

// PythonGradeTask represents a single task result from grade.py.
type PythonGradeTask struct {
	Score    int    `json:"score"`
	MaxScore int    `json:"max_score"`
	Passed   bool   `json:"passed"`
	Detail   string `json:"detail"`
}

// LabSubmitModuleRequest is the request to grade a specific module.
type LabSubmitModuleRequest struct {
	SubmissionID uuid.UUID `json:"submission_id"`
	ModuleNumber int       `json:"module_number"`
}
