package http

import (
	"context"
	"encoding/json"
	"errors"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"

	"github.com/go-chi/chi/v5"
	"github.com/google/uuid"
	"github.com/pashagolub/pgxmock/v5"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/netcert/backend/internal/repository/postgres"
	"github.com/netcert/backend/internal/usecase"
)

func TestExamHandler_ListTracks(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	now := time.Now()
	id := uuid.New()
	rows := pgxmock.NewRows([]string{"id", "slug", "vendor", "name", "description", "icon_url", "sort_order", "created_at"}).
		AddRow(id, "junos-ent", "juniper", "Enterprise", "Desc", nil, 1, now)

	pool.ExpectQuery(`SELECT .+ FROM tracks ORDER BY sort_order`).WillReturnRows(rows)

	examRepo := postgres.NewExamRepository(pool)
	attemptRepo := postgres.NewAttemptRepository(pool)
	examUC := usecase.NewExamUseCase(examRepo, attemptRepo)
	handler := NewExamHandler(examUC)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/tracks", nil)
	w := httptest.NewRecorder()

	handler.ListTracks(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var tracks interface{}
	err = json.NewDecoder(w.Body).Decode(&tracks)
	require.NoError(t, err)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamHandler_GetExam_Success(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	examID := uuid.New()
	trackID := uuid.New()
	rows := pgxmock.NewRows([]string{"id", "track_id", "code", "name", "level", "duration_minutes", "total_questions", "passing_score", "blueprint_url", "is_active", "created_at"}).
		AddRow(examID, trackID, "JN0-100", "JNCIA-Junos", "JNCIA", 90, 60, 65.0, nil, true, time.Now())

	pool.ExpectQuery(`SELECT .+ FROM exams WHERE id`).WithArgs(examID).WillReturnRows(rows)

	examRepo := postgres.NewExamRepository(pool)
	attemptRepo := postgres.NewAttemptRepository(pool)
	examUC := usecase.NewExamUseCase(examRepo, attemptRepo)
	handler := NewExamHandler(examUC)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/exams/"+examID.String(), nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("examId", examID.String())
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetExam(w, req)

	assert.Equal(t, http.StatusOK, w.Code)

	var exam map[string]interface{}
	json.NewDecoder(w.Body).Decode(&exam)
	assert.Equal(t, "JNCIA-Junos", exam["name"])
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamHandler_GetExam_NotFound(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	examID := uuid.New()

	pool.ExpectQuery(`SELECT .+ FROM exams WHERE id`).
		WithArgs(examID).
		WillReturnError(errors.New("exam not found"))

	examRepo := postgres.NewExamRepository(pool)
	attemptRepo := postgres.NewAttemptRepository(pool)
	examUC := usecase.NewExamUseCase(examRepo, attemptRepo)
	handler := NewExamHandler(examUC)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/exams/"+examID.String(), nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("examId", examID.String())
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetExam(w, req)

	assert.Equal(t, http.StatusNotFound, w.Code)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamHandler_GetExam_InvalidID(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	examRepo := postgres.NewExamRepository(pool)
	attemptRepo := postgres.NewAttemptRepository(pool)
	examUC := usecase.NewExamUseCase(examRepo, attemptRepo)
	handler := NewExamHandler(examUC)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/exams/not-a-uuid", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("examId", "not-a-uuid")
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetExam(w, req)

	assert.Equal(t, http.StatusBadRequest, w.Code)
}

func TestExamHandler_GetTrack(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	slug := "junos-ent"
	id := uuid.New()
	rows := pgxmock.NewRows([]string{"id", "slug", "vendor", "name", "description", "icon_url", "sort_order", "created_at"}).
		AddRow(id, slug, "juniper", "Enterprise", "Desc", nil, 1, time.Now())

	pool.ExpectQuery(`SELECT .+ FROM tracks WHERE slug`).WithArgs(slug).WillReturnRows(rows)

	examRepo := postgres.NewExamRepository(pool)
	attemptRepo := postgres.NewAttemptRepository(pool)
	examUC := usecase.NewExamUseCase(examRepo, attemptRepo)
	handler := NewExamHandler(examUC)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/tracks/"+slug, nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("slug", slug)
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.GetTrack(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamHandler_ListExams(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	slug := "junos-ent"
	trackID := uuid.New()

	// Find track by slug
	trackRows := pgxmock.NewRows([]string{"id", "slug", "vendor", "name", "description", "icon_url", "sort_order", "created_at"}).
		AddRow(trackID, slug, "juniper", "Enterprise", "Desc", nil, 1, time.Now())

	pool.ExpectQuery(`SELECT .+ FROM tracks WHERE slug`).WithArgs(slug).WillReturnRows(trackRows)

	// List exams
	examRows := pgxmock.NewRows([]string{"id", "track_id", "code", "name", "level", "duration_minutes", "total_questions", "passing_score", "blueprint_url", "is_active", "created_at"}).
		AddRow(uuid.New(), trackID, "JN0-100", "JNCIA", "JNCIA", 90, 60, 65.0, nil, true, time.Now())

	pool.ExpectQuery(`SELECT .+ FROM exams`).WithArgs(trackID).WillReturnRows(examRows)

	examRepo := postgres.NewExamRepository(pool)
	attemptRepo := postgres.NewAttemptRepository(pool)
	examUC := usecase.NewExamUseCase(examRepo, attemptRepo)
	handler := NewExamHandler(examUC)

	req := httptest.NewRequest(http.MethodGet, "/api/v1/tracks/"+slug+"/exams", nil)
	rctx := chi.NewRouteContext()
	rctx.URLParams.Add("slug", slug)
	req = req.WithContext(context.WithValue(req.Context(), chi.RouteCtxKey, rctx))
	w := httptest.NewRecorder()

	handler.ListExams(w, req)

	assert.Equal(t, http.StatusOK, w.Code)
	assert.NoError(t, pool.ExpectationsWereMet())
}
