package postgres

import (
	"context"
	"encoding/json"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

type ExplanationRepository struct {
	pool DBPool
}

func NewExplanationRepository(pool DBPool) *ExplanationRepository {
	return &ExplanationRepository{pool: pool}
}

// FindByQuestionID returns the latest active explanation for a question
func (r *ExplanationRepository) FindByQuestionID(ctx context.Context, questionID uuid.UUID) (*domain.Explanation, error) {
	query := `SELECT id, question_id, version, sections, summary, is_active, created_at, updated_at
		FROM explanations
		WHERE question_id = $1 AND is_active = true
		ORDER BY version DESC
		LIMIT 1`

	e := &domain.Explanation{}
	var sectionsBytes []byte
	err := r.pool.QueryRow(ctx, query, questionID).Scan(
		&e.ID, &e.QuestionID, &e.Version, &sectionsBytes,
		&e.Summary, &e.IsActive, &e.CreatedAt, &e.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}
	e.Sections = json.RawMessage(sectionsBytes)
	return e, nil
}

// FindVersionByQuestionID returns a specific version of an explanation
func (r *ExplanationRepository) FindVersionByQuestionID(ctx context.Context, questionID uuid.UUID, version int) (*domain.Explanation, error) {
	query := `SELECT id, question_id, version, sections, summary, is_active, created_at, updated_at
		FROM explanations
		WHERE question_id = $1 AND version = $2
		LIMIT 1`

	e := &domain.Explanation{}
	var sectionsBytes []byte
	err := r.pool.QueryRow(ctx, query, questionID, version).Scan(
		&e.ID, &e.QuestionID, &e.Version, &sectionsBytes,
		&e.Summary, &e.IsActive, &e.CreatedAt, &e.UpdatedAt,
	)
	if err != nil {
		return nil, err
	}
	e.Sections = json.RawMessage(sectionsBytes)
	return e, nil
}

// ListVersions returns all versions of explanations for a question
func (r *ExplanationRepository) ListVersions(ctx context.Context, questionID uuid.UUID) ([]domain.Explanation, error) {
	rows, err := r.pool.Query(ctx, `SELECT id, question_id, version, sections, summary, is_active, created_at, updated_at
		FROM explanations WHERE question_id = $1 ORDER BY version DESC`, questionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var explanations []domain.Explanation
	for rows.Next() {
		var e domain.Explanation
		var sectionsBytes []byte
		if err := rows.Scan(&e.ID, &e.QuestionID, &e.Version, &sectionsBytes,
			&e.Summary, &e.IsActive, &e.CreatedAt, &e.UpdatedAt); err != nil {
			return nil, err
		}
		e.Sections = json.RawMessage(sectionsBytes)
		explanations = append(explanations, e)
	}
	return explanations, nil
}

// SaveTelemetryEvents batch-inserts telemetry events
func (r *ExplanationRepository) SaveTelemetryEvents(ctx context.Context, userID uuid.UUID, events []domain.TelemetryEventPayload) error {
	query := `INSERT INTO explanation_telemetry
		(user_id, explanation_id, question_id, session_id, event_type, section_type, distractor_option_id, time_spent_seconds, metadata, created_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, NOW())`

	for _, e := range events {
		var explanationID, questionID *uuid.UUID
		if e.ExplanationID != "" {
			if uid, err := uuid.Parse(e.ExplanationID); err == nil {
				explanationID = &uid
			}
		}
		if e.QuestionID != "" {
			if uid, err := uuid.Parse(e.QuestionID); err == nil {
				questionID = &uid
			}
		}
		sessionID, _ := uuid.Parse(e.SessionID)

		metaBytes := e.Metadata
		if metaBytes == nil {
			metaBytes = json.RawMessage(`{}`)
		}

		_, err := r.pool.Exec(ctx, query,
			userID, explanationID, questionID, sessionID,
			e.EventType, e.SectionType, e.DistractorOptionID,
			e.TimeSpentSeconds, metaBytes,
		)
		if err != nil {
			return err
		}
	}
	return nil
}
