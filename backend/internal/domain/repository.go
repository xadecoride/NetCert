package domain

import (
	"context"
	"encoding/json"

	"github.com/google/uuid"
)

// UserRepository defines the contract for user persistence.
// Implementations live in infrastructure (e.g., postgres.UserRepository).
type UserRepository interface {
	Create(ctx context.Context, user *User) error
	FindByID(ctx context.Context, id uuid.UUID) (*User, error)
	FindByEmail(ctx context.Context, email string) (*User, error)
	Update(ctx context.Context, user *User) error
	UpdatePreferences(ctx context.Context, userID uuid.UUID, prefs json.RawMessage) error
}

// ExamRepository defines the contract for exam and question persistence.
type ExamRepository interface {
	ListTracks(ctx context.Context) ([]Track, error)
	FindTrackBySlug(ctx context.Context, slug string) (*Track, error)
	ListExams(ctx context.Context, trackID uuid.UUID) ([]Exam, error)
	FindExamByID(ctx context.Context, id uuid.UUID) (*Exam, error)
	ListQuestions(ctx context.Context, examID uuid.UUID) ([]Question, error)
	ListQuestionIDs(ctx context.Context, examID uuid.UUID) ([]uuid.UUID, error)
	ListQuestionIDsByType(ctx context.Context, examID uuid.UUID, questionType string) ([]uuid.UUID, error)
	GetQuestionsByIDs(ctx context.Context, ids []uuid.UUID) ([]Question, error)
	FindQuestionByID(ctx context.Context, id uuid.UUID) (*Question, error)
}

// AttemptRepository defines the contract for attempt and answer persistence.
type AttemptRepository interface {
	Create(ctx context.Context, a *Attempt) error
	FindByID(ctx context.Context, id uuid.UUID) (*Attempt, error)
	ListByUser(ctx context.Context, userID uuid.UUID) ([]Attempt, error)
	UpdateStatus(ctx context.Context, id uuid.UUID, status AttemptStatus) error
	Complete(ctx context.Context, id uuid.UUID, score float64, correct, answered int) error
	UpdateProgress(ctx context.Context, id uuid.UUID, answered, correct int) error
	SaveAnswer(ctx context.Context, a *AttemptAnswer) error
	GetAnswers(ctx context.Context, attemptID uuid.UUID) ([]AttemptAnswer, error)
	SaveAttemptQuestions(ctx context.Context, attemptID uuid.UUID, questionIDs []uuid.UUID) error
	GetAttemptQuestionIDs(ctx context.Context, attemptID uuid.UUID) ([]uuid.UUID, error)
	IsQuestionInAttempt(ctx context.Context, attemptID, questionID uuid.UUID) (bool, error)
	HasUserAnsweredQuestion(ctx context.Context, questionID, userID uuid.UUID) (bool, error)
	HasAnswer(ctx context.Context, attemptID, questionID uuid.UUID) (bool, error)
}

// ExplanationRepository defines the contract for explanation and telemetry persistence.
type ExplanationRepository interface {
	FindByQuestionID(ctx context.Context, questionID uuid.UUID) (*Explanation, error)
	FindVersionByQuestionID(ctx context.Context, questionID uuid.UUID, version int) (*Explanation, error)
	ListVersions(ctx context.Context, questionID uuid.UUID) ([]Explanation, error)
	SaveTelemetryEvents(ctx context.Context, userID uuid.UUID, events []TelemetryEventPayload) error
}

// StudyProgressRepository defines the contract for study progress persistence.
type StudyProgressRepository interface {
	ListByUser(ctx context.Context, userID uuid.UUID) ([]StudyProgress, error)
	Upsert(ctx context.Context, userID uuid.UUID, guideID string, completed bool) error
}
