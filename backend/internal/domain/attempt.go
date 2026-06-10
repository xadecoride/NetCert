package domain

import (
	"time"

	"github.com/google/uuid"
)

type AttemptStatus string

const (
	AttemptStatusInProgress AttemptStatus = "in_progress"
	AttemptStatusPaused     AttemptStatus = "paused"
	AttemptStatusCompleted  AttemptStatus = "completed"
	AttemptStatusTimedOut   AttemptStatus = "timed_out"
	AttemptStatusAbandoned  AttemptStatus = "abandoned"
)

type Attempt struct {
	ID                 uuid.UUID     `json:"id"`
	UserID             uuid.UUID     `json:"user_id"`
	ExamID             uuid.UUID     `json:"exam_id"`
	Status             AttemptStatus `json:"status"`
	Mode               string        `json:"mode"`
	StartedAt          time.Time     `json:"started_at"`
	CompletedAt        *time.Time    `json:"completed_at,omitempty"`
	DurationSeconds    int           `json:"duration_seconds"`
	Score              *float64      `json:"score,omitempty"`
	QuestionsTotal     int           `json:"questions_total"`
	QuestionsAnswered  int           `json:"questions_answered"`
	QuestionsCorrect   int           `json:"questions_correct"`
	QuestionsFlagged   []uuid.UUID   `json:"questions_flagged,omitempty"`
	CreatedAt          time.Time     `json:"created_at"`
}

type AttemptAnswer struct {
	ID              uuid.UUID  `json:"id"`
	AttemptID       uuid.UUID  `json:"attempt_id"`
	QuestionID      uuid.UUID  `json:"question_id"`
	UserAnswer      string     `json:"user_answer"`
	IsCorrect       *bool      `json:"is_correct,omitempty"`
	TimeSpentSeconds int       `json:"time_spent_seconds"`
	WasFlagged      bool       `json:"was_flagged"`
	CreatedAt       time.Time  `json:"created_at"`
}

type AttemptReview struct {
	ID         uuid.UUID  `json:"id"`
	AttemptID  uuid.UUID  `json:"attempt_id"`
	UserID     uuid.UUID  `json:"user_id"`
	QuestionID uuid.UUID  `json:"question_id"`
	UserNotes  *string    `json:"user_notes,omitempty"`
	IsBookmarked bool     `json:"is_bookmarked"`
	Rating     *int       `json:"rating,omitempty"`
	CreatedAt  time.Time  `json:"created_at"`
}

// AttemptWithDetails combines attempt data with questions and user answers for review
type AttemptWithDetails struct {
	Attempt
	Questions []AttemptQuestionWithAnswer `json:"questions"`
}

type AttemptQuestionWithAnswer struct {
	ID              uuid.UUID        `json:"id"`
	Body            string           `json:"body"`
	Options         []QuestionOption `json:"options,omitempty"`
	QuestionType    QuestionType     `json:"question_type"`
	Difficulty      int              `json:"difficulty"`
	Explanation     string           `json:"explanation"`
	ReferenceURLs   []string         `json:"reference_urls,omitempty"`
	BlueprintSection string           `json:"blueprint_section"`
	UserAnswer      string           `json:"user_answer"`
	IsCorrect       *bool            `json:"is_correct"`
	WasFlagged      bool             `json:"was_flagged"`
	TimeSpentSeconds int             `json:"time_spent_seconds"`
}

type StartAttemptRequest struct {
	ExamID        uuid.UUID `json:"exam_id" validate:"required"`
	Mode          string    `json:"mode" validate:"required,oneof=exam practice timed"`
	QuestionCount int       `json:"question_count"` // optional override; uses exam total if 0
}

type SubmitAnswerRequest struct {
	QuestionID       uuid.UUID `json:"question_id" validate:"required"`
	Answer           string    `json:"answer" validate:"required"`
	TimeSpentSeconds int       `json:"time_spent_seconds" validate:"required"`
	WasFlagged       bool      `json:"was_flagged"`
}
