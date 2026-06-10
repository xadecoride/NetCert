package domain

import (
	"encoding/json"
	"time"

	"github.com/google/uuid"
)

// ExplanationSectionType defines the type of content section in an explanation
type ExplanationSectionType string

const (
	ExplanationSectionTLDR              ExplanationSectionType = "tl_dr"
	ExplanationSectionScenario          ExplanationSectionType = "scenario"
	ExplanationSectionWhyCorrect        ExplanationSectionType = "why_correct"
	ExplanationSectionDistractorAnalysis ExplanationSectionType = "distractor_analysis"
	ExplanationSectionCLIExamples       ExplanationSectionType = "cli_examples"
	ExplanationSectionVisualization     ExplanationSectionType = "visualization"
	ExplanationSectionVendorNuances     ExplanationSectionType = "vendor_nuances"
)

// ExplanationSection represents a single section within a deep-dive explanation
type ExplanationSection struct {
	SectionType  ExplanationSectionType `json:"section_type"`
	Title        string                 `json:"title"`
	Content      string                 `json:"content"`
	IsCollapsible bool                  `json:"is_collapsible"`
	SortOrder    int                    `json:"sort_order"`
}

// DistractorAnalysis is the content structure for distractor_analysis sections
type DistractorAnalysis struct {
	OptionID     string `json:"option_id"`
	WhyWrong     string `json:"why_wrong"`
	CommonMistake bool   `json:"common_mistake"`
}

// Explanation represents a versioned deep-dive explanation attached to a question
type Explanation struct {
	ID         uuid.UUID       `json:"id"`
	QuestionID uuid.UUID       `json:"question_id"`
	Version    int             `json:"version"`
	Sections   json.RawMessage `json:"sections"`
	Summary    string          `json:"summary"`
	IsActive   bool            `json:"is_active"`
	CreatedAt  time.Time       `json:"created_at"`
	UpdatedAt  time.Time       `json:"updated_at"`
}

// ExplanationTelemetryEvent represents a single telemetry event from user interaction
type ExplanationTelemetryEvent struct {
	ID                 uuid.UUID `json:"id"`
	UserID             uuid.UUID `json:"user_id"`
	ExplanationID      *uuid.UUID `json:"explanation_id,omitempty"`
	QuestionID         *uuid.UUID `json:"question_id,omitempty"`
	SessionID          uuid.UUID `json:"session_id"`
	EventType          string    `json:"event_type"`
	SectionType        string    `json:"section_type,omitempty"`
	DistractorOptionID string    `json:"distractor_option_id,omitempty"`
	TimeSpentSeconds   int       `json:"time_spent_seconds"`
	Metadata           json.RawMessage `json:"metadata,omitempty"`
	CreatedAt          time.Time `json:"created_at"`
}

// BatchTelemetryRequest is the request body for batch telemetry submission
type BatchTelemetryRequest struct {
	Events []TelemetryEventPayload `json:"events" validate:"required,max=50"`
}

// TelemetryEventPayload is a single event in a batch submission
type TelemetryEventPayload struct {
	QuestionID         string `json:"question_id"`
	ExplanationID      string `json:"explanation_id,omitempty"`
	SessionID          string `json:"session_id"`
	EventType          string `json:"event_type" validate:"required"`
	SectionType        string `json:"section_type,omitempty"`
	DistractorOptionID string `json:"distractor_option_id,omitempty"`
	TimeSpentSeconds   int    `json:"time_spent_seconds"`
	Metadata           json.RawMessage `json:"metadata,omitempty"`
}
