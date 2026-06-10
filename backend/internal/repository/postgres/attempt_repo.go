package postgres

import (
	"context"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/netcert/backend/internal/domain"
)

type AttemptRepository struct {
	pool DBPool
}

func NewAttemptRepository(pool DBPool) *AttemptRepository {
	return &AttemptRepository{pool: pool}
}

func (r *AttemptRepository) Create(ctx context.Context, a *domain.Attempt) error {
	query := `INSERT INTO attempts (id, user_id, exam_id, status, mode, started_at, duration_seconds, questions_total, questions_answered, questions_correct, created_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11)`
	_, err := r.pool.Exec(ctx, query,
		a.ID, a.UserID, a.ExamID, a.Status, a.Mode, a.StartedAt, a.DurationSeconds,
		a.QuestionsTotal, a.QuestionsAnswered, a.QuestionsCorrect, a.CreatedAt,
	)
	return err
}

func (r *AttemptRepository) FindByID(ctx context.Context, id uuid.UUID) (*domain.Attempt, error) {
	query := `SELECT id, user_id, exam_id, status, mode, started_at, completed_at, duration_seconds, score, questions_total, questions_answered, questions_correct, questions_flagged, created_at
		FROM attempts WHERE id = $1`
	a := &domain.Attempt{}
	err := r.pool.QueryRow(ctx, query, id).Scan(
		&a.ID, &a.UserID, &a.ExamID, &a.Status, &a.Mode, &a.StartedAt, &a.CompletedAt,
		&a.DurationSeconds, &a.Score, &a.QuestionsTotal, &a.QuestionsAnswered, &a.QuestionsCorrect,
		&a.QuestionsFlagged, &a.CreatedAt,
	)
	if err != nil {
		return nil, err
	}
	return a, nil
}

func (r *AttemptRepository) ListByUser(ctx context.Context, userID uuid.UUID) ([]domain.Attempt, error) {
	rows, err := r.pool.Query(ctx, `SELECT id, user_id, exam_id, status, mode, started_at, completed_at, duration_seconds, score, questions_total, questions_answered, questions_correct, questions_flagged, created_at
		FROM attempts WHERE user_id = $1 ORDER BY created_at DESC`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var attempts []domain.Attempt
	for rows.Next() {
		var a domain.Attempt
		if err := rows.Scan(&a.ID, &a.UserID, &a.ExamID, &a.Status, &a.Mode, &a.StartedAt, &a.CompletedAt,
			&a.DurationSeconds, &a.Score, &a.QuestionsTotal, &a.QuestionsAnswered, &a.QuestionsCorrect,
			&a.QuestionsFlagged, &a.CreatedAt); err != nil {
			return nil, err
		}
		attempts = append(attempts, a)
	}
	return attempts, nil
}

func (r *AttemptRepository) UpdateStatus(ctx context.Context, id uuid.UUID, status domain.AttemptStatus) error {
	_, err := r.pool.Exec(ctx, `UPDATE attempts SET status=$1 WHERE id=$2`, status, id)
	return err
}

func (r *AttemptRepository) Complete(ctx context.Context, id uuid.UUID, score float64, correct, answered int) error {
	_, err := r.pool.Exec(ctx, `UPDATE attempts SET status=$1, score=$2, questions_correct=$3, questions_answered=$4, completed_at=NOW() WHERE id=$5`,
		domain.AttemptStatusCompleted, score, correct, answered, id)
	return err
}

func (r *AttemptRepository) UpdateProgress(ctx context.Context, id uuid.UUID, answered, correct int) error {
	_, err := r.pool.Exec(ctx, `UPDATE attempts SET questions_answered=$1, questions_correct=$2 WHERE id=$3`,
		answered, correct, id)
	return err
}

func (r *AttemptRepository) SaveAnswer(ctx context.Context, a *domain.AttemptAnswer) error {
	query := `INSERT INTO attempt_answers (id, attempt_id, question_id, user_answer, is_correct, time_spent_seconds, was_flagged, created_at)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)`
	_, err := r.pool.Exec(ctx, query, a.ID, a.AttemptID, a.QuestionID, a.UserAnswer, a.IsCorrect, a.TimeSpentSeconds, a.WasFlagged, a.CreatedAt)
	return err
}

func (r *AttemptRepository) GetAnswers(ctx context.Context, attemptID uuid.UUID) ([]domain.AttemptAnswer, error) {
	rows, err := r.pool.Query(ctx, `SELECT id, attempt_id, question_id, user_answer, is_correct, time_spent_seconds, was_flagged, created_at
		FROM attempt_answers WHERE attempt_id = $1 ORDER BY created_at`, attemptID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var answers []domain.AttemptAnswer
	for rows.Next() {
		var a domain.AttemptAnswer
		if err := rows.Scan(&a.ID, &a.AttemptID, &a.QuestionID, &a.UserAnswer, &a.IsCorrect, &a.TimeSpentSeconds, &a.WasFlagged, &a.CreatedAt); err != nil {
			return nil, err
		}
		answers = append(answers, a)
	}
	return answers, nil
}

// SaveAttemptQuestions stores the randomly selected question IDs for an attempt (batch insert)
func (r *AttemptRepository) SaveAttemptQuestions(ctx context.Context, attemptID uuid.UUID, questionIDs []uuid.UUID) error {
	if len(questionIDs) == 0 {
		return nil
	}
	// Batch insert using pgx.CopyFrom for efficiency (single round-trip)
	rows := make([][]interface{}, len(questionIDs))
	for i, qID := range questionIDs {
		rows[i] = []interface{}{attemptID, qID, int16(i)}
	}
	_, err := r.pool.CopyFrom(
		ctx,
		pgx.Identifier{"attempt_questions"},
		[]string{"attempt_id", "question_id", "order_index"},
		pgx.CopyFromRows(rows),
	)
	return err
}

// GetAttemptQuestionIDs returns the ordered question IDs for an attempt
func (r *AttemptRepository) GetAttemptQuestionIDs(ctx context.Context, attemptID uuid.UUID) ([]uuid.UUID, error) {
	rows, err := r.pool.Query(ctx, `SELECT question_id FROM attempt_questions WHERE attempt_id = $1 ORDER BY order_index`, attemptID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var ids []uuid.UUID
	for rows.Next() {
		var id uuid.UUID
		if err := rows.Scan(&id); err != nil {
			return nil, err
		}
		ids = append(ids, id)
	}
	return ids, nil
}

// IsQuestionInAttempt checks if a question belongs to the attempt's selected subset
func (r *AttemptRepository) IsQuestionInAttempt(ctx context.Context, attemptID, questionID uuid.UUID) (bool, error) {
	var exists bool
	err := r.pool.QueryRow(ctx, `SELECT EXISTS(
		SELECT 1 FROM attempt_questions WHERE attempt_id = $1 AND question_id = $2
	)`, attemptID, questionID).Scan(&exists)
	if err != nil {
		return false, err
	}
	return exists, nil
}

// HasUserAnsweredQuestion checks if a user has answered a specific question in any attempt
func (r *AttemptRepository) HasUserAnsweredQuestion(ctx context.Context, questionID, userID uuid.UUID) (bool, error) {
	var exists bool
	err := r.pool.QueryRow(ctx, `SELECT EXISTS(
		SELECT 1 FROM attempt_answers aa
		JOIN attempts a ON a.id = aa.attempt_id
		WHERE aa.question_id = $1 AND a.user_id = $2
	)`, questionID, userID).Scan(&exists)
	if err != nil {
		return false, err
	}
	return exists, nil
}

// HasAnswer checks if an attempt already has an answer for a specific question.
func (r *AttemptRepository) HasAnswer(ctx context.Context, attemptID, questionID uuid.UUID) (bool, error) {
	var exists bool
	err := r.pool.QueryRow(ctx, `SELECT EXISTS(
		SELECT 1 FROM attempt_answers WHERE attempt_id = $1 AND question_id = $2
	)`, attemptID, questionID).Scan(&exists)
	if err != nil {
		return false, err
	}
	return exists, nil
}
