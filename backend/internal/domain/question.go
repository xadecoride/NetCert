package domain

import (
	"time"

	"github.com/google/uuid"
)

type QuestionType string

const (
	QuestionTypeSingleChoice   QuestionType = "single-choice"
	QuestionTypeMultipleChoice QuestionType = "multiple-choice"
	QuestionTypeDragDrop       QuestionType = "drag-drop"
	QuestionTypeFillBlank      QuestionType = "fill-blank"
	QuestionTypeSimlet         QuestionType = "simlet"
)

type BloomLevel string

const (
	BloomRemember    BloomLevel = "remember"
	BloomUnderstand  BloomLevel = "understand"
	BloomApply       BloomLevel = "apply"
	BloomAnalyze     BloomLevel = "analyze"
	BloomTroubleshoot BloomLevel = "troubleshoot"
	BloomDesign      BloomLevel = "design"
)

type Question struct {
	ID                uuid.UUID           `json:"id"`
	ExamID            uuid.UUID           `json:"exam_id"`
	TrackID           uuid.UUID           `json:"track_id"`
	QuestionType      QuestionType        `json:"question_type"`
	Difficulty        int                 `json:"difficulty"`
	BloomLevel        BloomLevel          `json:"bloom_level"`
	Body              string              `json:"body"`
	Options           []QuestionOption    `json:"options,omitempty"`
	Explanation       string              `json:"explanation"`
	ReferenceURLs     []string            `json:"reference_urls,omitempty"`
	BlueprintSection  string              `json:"blueprint_section"`
	BlueprintWeight   float64             `json:"blueprint_weight"`
	IsActive          bool                `json:"is_active"`
	Tags              []string            `json:"tags,omitempty"`
	CreatedAt         time.Time           `json:"created_at"`
	UpdatedAt         time.Time           `json:"updated_at"`
}

type QuestionOption struct {
	ID      string `json:"id"`
	Text    string `json:"text"`
	IsCorrect bool  `json:"is_correct,omitempty"`
}

type QuestionTag struct {
	ID         uuid.UUID `json:"id"`
	QuestionID uuid.UUID `json:"question_id"`
	Technology string    `json:"technology"`
	Protocol   string    `json:"protocol"`
}
