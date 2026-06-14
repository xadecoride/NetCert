package domain

import (
	"time"

	"github.com/google/uuid"
)

// QuickLabTask represents a single task within a QuickLab.
type QuickLabTask struct {
	Order                int      `json:"order"`
	Title                string   `json:"title"`
	Description          string   `json:"description"`
	VerificationCommands []string `json:"verification_commands,omitempty"`
	ExpectedOutputSummary string  `json:"expected_output_summary,omitempty"`
}

// QuickLabHint represents a progressive hint for a QuickLab.
type QuickLabHint struct {
	Order int    `json:"order"`
	Title string `json:"title"`
	Content string `json:"content"`
}

// QuickLabAnswer represents the answer for a specific task.
type QuickLabAnswer struct {
	Order      int    `json:"order"`
	TaskOrder  int    `json:"task_order"`
	Content    string `json:"content"`
}

// QuickLabExplanation represents a detailed explanation/breakdown.
type QuickLabExplanation struct {
	Order   int    `json:"order"`
	Title   string `json:"title"`
	Content string `json:"content"`
}

// QuickLabSolutionCommand represents solution commands for a task.
type QuickLabSolutionCommand struct {
	Order           int      `json:"order"`
	TaskOrder       int      `json:"task_order"`
	Commands        []string `json:"commands"`
	ExpectedOutput  string   `json:"expected_output,omitempty"`
}

// QuickLab represents a self-paced PNETlab-compatible exercise.
type QuickLab struct {
	ID                  uuid.UUID                  `json:"id"`
	TrackID             uuid.UUID                  `json:"track_id"`
	Slug                string                     `json:"slug"`
	Title               string                     `json:"title"`
	Description         string                     `json:"description"`
	Level               Level                      `json:"level"`
	Difficulty          int                        `json:"difficulty"`
	EstimatedMinutes    int                        `json:"estimated_minutes"`
	Technology          string                     `json:"technology"`
	TopologySVG         string                     `json:"topology_svg,omitempty"`
	PnetlabInstructions string                     `json:"pnetlab_instructions"`
	Tasks               []QuickLabTask             `json:"tasks,omitempty"`
	Hints               []QuickLabHint             `json:"hints,omitempty"`
	Answers             []QuickLabAnswer           `json:"answers,omitempty"`
	Explanations        []QuickLabExplanation      `json:"explanations,omitempty"`
	SolutionCommands    []QuickLabSolutionCommand  `json:"solution_commands,omitempty"`
	PrerequisiteTopics  []string                   `json:"prerequisite_topics,omitempty"`
	IsActive            bool                       `json:"is_active"`
	CreatedAt           time.Time                  `json:"created_at"`
	UpdatedAt           time.Time                  `json:"updated_at"`
}
