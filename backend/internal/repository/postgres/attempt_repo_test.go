package postgres

import (
	"context"
	"errors"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/pashagolub/pgxmock/v5"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/netcert/backend/internal/domain"
)

func TestAttemptRepository_Create(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()

	now := time.Now()
	attempt := &domain.Attempt{
		ID:                uuid.New(),
		UserID:            uuid.New(),
		ExamID:            uuid.New(),
		Status:            domain.AttemptStatusInProgress,
		Mode:              "exam",
		StartedAt:         now,
		DurationSeconds:   5400,
		QuestionsTotal:    60,
		QuestionsAnswered: 0,
		QuestionsCorrect:  0,
		CreatedAt:         now,
	}

	pool.ExpectExec(`INSERT INTO attempts`).
		WithArgs(attempt.ID, attempt.UserID, attempt.ExamID, attempt.Status, attempt.Mode,
			attempt.StartedAt, attempt.DurationSeconds, attempt.QuestionsTotal,
			attempt.QuestionsAnswered, attempt.QuestionsCorrect, attempt.CreatedAt).
		WillReturnResult(pgxmock.NewResult("INSERT", 1))

	err = repo.Create(ctx, attempt)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_FindByID(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()
	id := uuid.New()

	now := time.Now()
	score := 85.5
	rows := pgxmock.NewRows([]string{
		"id", "user_id", "exam_id", "status", "mode", "started_at", "completed_at",
		"duration_seconds", "score", "questions_total", "questions_answered",
		"questions_correct", "questions_flagged", "created_at",
	}).AddRow(id, uuid.New(), uuid.New(), "completed", "exam", now, &now,
		3600, &score, 60, 60, 51, []uuid.UUID{}, now)

	pool.ExpectQuery(`SELECT .+ FROM attempts WHERE id`).WithArgs(id).WillReturnRows(rows)

	attempt, err := repo.FindByID(ctx, id)
	require.NoError(t, err)
	assert.Equal(t, id, attempt.ID)
	assert.Equal(t, domain.AttemptStatusCompleted, attempt.Status)
	assert.NotNil(t, attempt.Score)
	assert.Equal(t, 85.5, *attempt.Score)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_SaveAnswer(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()

	isCorrect := true
	answer := &domain.AttemptAnswer{
		ID:               uuid.New(),
		AttemptID:        uuid.New(),
		QuestionID:       uuid.New(),
		UserAnswer:       "A",
		IsCorrect:        &isCorrect,
		TimeSpentSeconds: 45,
		WasFlagged:       false,
		CreatedAt:        time.Now(),
	}

	pool.ExpectExec(`INSERT INTO attempt_answers`).
		WithArgs(answer.ID, answer.AttemptID, answer.QuestionID, answer.UserAnswer,
			answer.IsCorrect, answer.TimeSpentSeconds, answer.WasFlagged, answer.CreatedAt).
		WillReturnResult(pgxmock.NewResult("INSERT", 1))

	err = repo.SaveAnswer(ctx, answer)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_GetAnswers(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()
	attemptID := uuid.New()

	isCorrect := true
	now := time.Now()
	rows := pgxmock.NewRows([]string{
		"id", "attempt_id", "question_id", "user_answer", "is_correct",
		"time_spent_seconds", "was_flagged", "created_at",
	}).AddRow(uuid.New(), attemptID, uuid.New(), "A", &isCorrect, 30, false, now)

	pool.ExpectQuery(`SELECT .+ FROM attempt_answers WHERE attempt_id`).
		WithArgs(attemptID).WillReturnRows(rows)

	answers, err := repo.GetAnswers(ctx, attemptID)
	require.NoError(t, err)
	assert.Len(t, answers, 1)
	assert.True(t, *answers[0].IsCorrect)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_HasAnswer(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()
	attemptID := uuid.New()
	questionID := uuid.New()

	rows := pgxmock.NewRows([]string{"exists"}).AddRow(true)
	pool.ExpectQuery(`SELECT EXISTS`).WithArgs(attemptID, questionID).WillReturnRows(rows)

	exists, err := repo.HasAnswer(ctx, attemptID, questionID)
	require.NoError(t, err)
	assert.True(t, exists)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_HasAnswer_False(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()
	attemptID := uuid.New()
	questionID := uuid.New()

	rows := pgxmock.NewRows([]string{"exists"}).AddRow(false)
	pool.ExpectQuery(`SELECT EXISTS`).WithArgs(attemptID, questionID).WillReturnRows(rows)

	exists, err := repo.HasAnswer(ctx, attemptID, questionID)
	require.NoError(t, err)
	assert.False(t, exists)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_Complete(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()
	id := uuid.New()

	pool.ExpectExec(`UPDATE attempts SET status`).
		WithArgs(domain.AttemptStatusCompleted, 85.0, 51, 60, id).
		WillReturnResult(pgxmock.NewResult("UPDATE", 1))

	err = repo.Complete(ctx, id, 85.0, 51, 60)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_UpdateProgress(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()
	id := uuid.New()

	pool.ExpectExec(`UPDATE attempts SET questions_answered`).
		WithArgs(10, 7, id).
		WillReturnResult(pgxmock.NewResult("UPDATE", 1))

	err = repo.UpdateProgress(ctx, id, 10, 7)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_IsQuestionInAttempt(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()
	attemptID := uuid.New()
	questionID := uuid.New()

	rows := pgxmock.NewRows([]string{"exists"}).AddRow(true)
	pool.ExpectQuery(`SELECT EXISTS`).WithArgs(attemptID, questionID).WillReturnRows(rows)

	exists, err := repo.IsQuestionInAttempt(ctx, attemptID, questionID)
	require.NoError(t, err)
	assert.True(t, exists)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAttemptRepository_FindByID_Error(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewAttemptRepository(pool)
	ctx := context.Background()

	pool.ExpectQuery(`SELECT .+ FROM attempts WHERE id`).
		WithArgs(uuid.Nil).
		WillReturnError(errors.New("not found"))

	attempt, err := repo.FindByID(ctx, uuid.Nil)
	assert.Error(t, err)
	assert.Nil(t, attempt)
	assert.NoError(t, pool.ExpectationsWereMet())
}
