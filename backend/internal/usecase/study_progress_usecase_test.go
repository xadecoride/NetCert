package usecase

import (
	"context"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/pashagolub/pgxmock/v5"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/netcert/backend/internal/domain"
	"github.com/netcert/backend/internal/repository/postgres"
)

func TestStudyProgressUseCase_GetProgress(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	userID := uuid.New()
	now := time.Now()
	rows := pgxmock.NewRows([]string{"id", "user_id", "guide_id", "completed_at", "created_at"}).
		AddRow(uuid.New(), userID, "junos-cli", now, now).
		AddRow(uuid.New(), userID, "ospf", now, now)

	pool.ExpectQuery(`SELECT .+ FROM study_progress WHERE user_id`).
		WithArgs(userID).WillReturnRows(rows)

	repo := postgres.NewStudyProgressRepository(pool)
	uc := NewStudyProgressUseCase(repo)

	progress, err := uc.GetProgress(context.Background(), userID)
	require.NoError(t, err)
	assert.Len(t, progress, 2)
	assert.Equal(t, "junos-cli", progress[0].GuideID)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestStudyProgressUseCase_GetProgress_Empty(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	rows := pgxmock.NewRows([]string{"id", "user_id", "guide_id", "completed_at", "created_at"})
	pool.ExpectQuery(`SELECT .+ FROM study_progress WHERE user_id`).
		WithArgs(uuid.Nil).WillReturnRows(rows)

	repo := postgres.NewStudyProgressRepository(pool)
	uc := NewStudyProgressUseCase(repo)

	progress, err := uc.GetProgress(context.Background(), uuid.Nil)
	require.NoError(t, err)
	assert.Empty(t, progress)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestStudyProgressUseCase_ToggleGuide_Complete(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	userID := uuid.New()

	pool.ExpectExec(`INSERT INTO study_progress`).
		WithArgs(userID, "bgp").
		WillReturnResult(pgxmock.NewResult("INSERT", 1))

	repo := postgres.NewStudyProgressRepository(pool)
	uc := NewStudyProgressUseCase(repo)

	err = uc.ToggleGuide(context.Background(), userID, domain.StudyProgressToggleRequest{
		GuideID:  "bgp",
		Completed: true,
	})
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestStudyProgressUseCase_ToggleGuide_Uncomplete(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	userID := uuid.New()

	pool.ExpectExec(`DELETE FROM study_progress`).
		WithArgs(userID, "bgp").
		WillReturnResult(pgxmock.NewResult("DELETE", 1))

	repo := postgres.NewStudyProgressRepository(pool)
	uc := NewStudyProgressUseCase(repo)

	err = uc.ToggleGuide(context.Background(), userID, domain.StudyProgressToggleRequest{
		GuideID:  "bgp",
		Completed: false,
	})
	assert.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}
