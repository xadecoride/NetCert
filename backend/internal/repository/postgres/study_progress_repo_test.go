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
)

func TestStudyProgressRepository_ListByUser(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewStudyProgressRepository(pool)
	ctx := context.Background()
	userID := uuid.New()

	now := time.Now()
	rows := pgxmock.NewRows([]string{"id", "user_id", "guide_id", "completed_at", "created_at"}).
		AddRow(uuid.New(), userID, "junos-cli", now, now).
		AddRow(uuid.New(), userID, "ospf", now, now)

	pool.ExpectQuery(`SELECT .+ FROM study_progress WHERE user_id`).
		WithArgs(userID).WillReturnRows(rows)

	progress, err := repo.ListByUser(ctx, userID)
	require.NoError(t, err)
	assert.Len(t, progress, 2)
	assert.Equal(t, "junos-cli", progress[0].GuideID)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestStudyProgressRepository_ListByUser_Empty(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewStudyProgressRepository(pool)
	ctx := context.Background()

	userID := uuid.New()
	rows := pgxmock.NewRows([]string{"id", "user_id", "guide_id", "completed_at", "created_at"})
	pool.ExpectQuery(`SELECT .+ FROM study_progress WHERE user_id`).
		WithArgs(userID).WillReturnRows(rows)

	progress, err := repo.ListByUser(ctx, userID)
	require.NoError(t, err)
	assert.Empty(t, progress)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestStudyProgressRepository_Upsert_Completed(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewStudyProgressRepository(pool)
	ctx := context.Background()
	userID := uuid.New()

	pool.ExpectExec(`INSERT INTO study_progress`).
		WithArgs(userID, "bgp").
		WillReturnResult(pgxmock.NewResult("INSERT", 1))

	err = repo.Upsert(ctx, userID, "bgp", true)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestStudyProgressRepository_Upsert_NotCompleted(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewStudyProgressRepository(pool)
	ctx := context.Background()
	userID := uuid.New()

	pool.ExpectExec(`DELETE FROM study_progress`).
		WithArgs(userID, "isis").
		WillReturnResult(pgxmock.NewResult("DELETE", 1))

	err = repo.Upsert(ctx, userID, "isis", false)
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestStudyProgressRepository_ListByUser_Error(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewStudyProgressRepository(pool)
	ctx := context.Background()

	pool.ExpectQuery(`SELECT .+ FROM study_progress WHERE user_id`).
		WithArgs(uuid.Nil).
		WillReturnError(errors.New("connection refused"))

	progress, err := repo.ListByUser(ctx, uuid.Nil)
	assert.Error(t, err)
	assert.Nil(t, progress)
	assert.NoError(t, pool.ExpectationsWereMet())
}
