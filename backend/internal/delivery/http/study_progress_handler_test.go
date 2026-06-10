package http

import (
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/pashagolub/pgxmock/v5"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/netcert/backend/internal/repository/postgres"
	"github.com/netcert/backend/internal/usecase"
)

func TestStudyProgressHandler_GetProgress(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	now := time.Now()
	// Handler calls middleware.GetUserID() which returns uuid.Nil without auth middleware
	rows := pgxmock.NewRows([]string{"id", "user_id", "guide_id", "completed_at", "created_at"}).
		AddRow(uuid.New(), uuid.Nil, "junos-cli", now, now)

	pool.ExpectQuery(`SELECT .+ FROM study_progress WHERE user_id`).
		WithArgs(uuid.Nil).WillReturnRows(rows)

	repo := postgres.NewStudyProgressRepository(pool)
	uc := usecase.NewStudyProgressUseCase(repo)
	handler := NewStudyProgressHandler(uc)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/study/progress", nil)
	w := httptest.NewRecorder()

	handler.GetProgress(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestStudyProgressHandler_ToggleGuide(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	// Handler calls middleware.GetUserID() which returns uuid.Nil without auth middleware
	pool.ExpectExec(`INSERT INTO study_progress`).
		WithArgs(uuid.Nil, "bgp").
		WillReturnResult(pgxmock.NewResult("INSERT", 1))

	repo := postgres.NewStudyProgressRepository(pool)
	uc := usecase.NewStudyProgressUseCase(repo)
	handler := NewStudyProgressHandler(uc)

	body := `{"guide_id":"bgp","completed":true}`
	req := httptest.NewRequest(http.MethodPost, "/api/v1/study/progress/toggle", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.ToggleGuide(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAuthHandler_GetProfile(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	jwtMgr := testJWTManager()

	// Handler calls middleware.GetUserID() which returns uuid.Nil without auth middleware
	rows := pgxmock.NewRows([]string{
		"id", "email", "password_hash", "display_name", "role", "avatar_url",
		"oauth_provider", "oauth_id", "is_email_verified", "streak_days",
		"total_xp", "preferences", "created_at", "updated_at",
	}).AddRow(uuid.Nil, "test@example.com", "hash", "Test User", "student", nil, nil, nil, true, 0, 0, nil, time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM users WHERE id`).WithArgs(uuid.Nil).WillReturnRows(rows)

	userRepo := postgres.NewUserRepository(pool)
	authUC := usecase.NewAuthUseCase(userRepo, jwtMgr)
	handler := NewAuthHandler(authUC)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/users/me", nil)
	w := httptest.NewRecorder()

	handler.GetProfile(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestAuthHandler_UpdatePreferences(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	// Handler calls middleware.GetUserID() which returns uuid.Nil without auth middleware
	pool.ExpectExec(`UPDATE users SET preferences`).
		WithArgs(json.RawMessage(`{"language":"ru"}`), pgxmock.AnyArg(), uuid.Nil).
		WillReturnResult(pgxmock.NewResult("UPDATE", 1))

	rows := pgxmock.NewRows([]string{
		"id", "email", "password_hash", "display_name", "role", "avatar_url",
		"oauth_provider", "oauth_id", "is_email_verified", "streak_days",
		"total_xp", "preferences", "created_at", "updated_at",
	}).AddRow(uuid.Nil, "test@example.com", "hash", "Test", "student", nil, nil, nil, true, 0, 0, json.RawMessage(`{"language":"ru"}`), time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM users WHERE id`).WithArgs(uuid.Nil).WillReturnRows(rows)

	jwtMgr := testJWTManager()
	userRepo := postgres.NewUserRepository(pool)
	authUC := usecase.NewAuthUseCase(userRepo, jwtMgr)
	handler := NewAuthHandler(authUC)

	body := `{"language":"ru"}`
	req := httptest.NewRequest(http.MethodPut, "/api/v1/users/me/preferences", strings.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	w := httptest.NewRecorder()

	handler.UpdatePreferences(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.NoError(t, pool.ExpectationsWereMet())
}


