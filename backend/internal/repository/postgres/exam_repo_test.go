package postgres

import (
	"context"
	"encoding/json"
	"errors"
	"testing"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/pashagolub/pgxmock/v5"
	"github.com/stretchr/testify/assert"
	"github.com/stretchr/testify/require"

	"github.com/netcert/backend/internal/domain"
)

func TestExamRepository_ListTracks(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()

	now := time.Now()
	rows := pgxmock.NewRows([]string{"id", "slug", "vendor", "name", "description", "icon_url", "sort_order", "created_at"}).
		AddRow(uuid.New(), "junos-ent", "juniper", "Enterprise", "Juniper Enterprise track", nil, 1, now).
		AddRow(uuid.New(), "junos-sp", "juniper", "Service Provider", "Service Provider track", nil, 2, now)

	pool.ExpectQuery(`SELECT .+ FROM tracks ORDER BY sort_order`).WillReturnRows(rows)

	tracks, err := repo.ListTracks(ctx)
	require.NoError(t, err)
	assert.Len(t, tracks, 2)
	assert.Equal(t, "Enterprise", tracks[0].Name)
	assert.Equal(t, domain.Vendor("juniper"), tracks[0].Vendor)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_ListTracks_Empty(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()

	rows := pgxmock.NewRows([]string{"id", "slug", "vendor", "name", "description", "icon_url", "sort_order", "created_at"})
	pool.ExpectQuery(`SELECT .+ FROM tracks ORDER BY sort_order`).WillReturnRows(rows)

	tracks, err := repo.ListTracks(ctx)
	require.NoError(t, err)
	assert.Empty(t, tracks)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_FindTrackBySlug(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()
	slug := "junos-ent"
	id := uuid.New()

	rows := pgxmock.NewRows([]string{"id", "slug", "vendor", "name", "description", "icon_url", "sort_order", "created_at"}).
		AddRow(id, slug, "juniper", "Enterprise", "Desc", nil, 1, time.Now())

	pool.ExpectQuery(`SELECT .+ FROM tracks WHERE slug`).WithArgs(slug).WillReturnRows(rows)

	track, err := repo.FindTrackBySlug(ctx, slug)
	require.NoError(t, err)
	assert.Equal(t, id, track.ID)
	assert.Equal(t, slug, track.Slug)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_FindTrackBySlug_NotFound(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()

	pool.ExpectQuery(`SELECT .+ FROM tracks WHERE slug`).
		WithArgs("nonexistent").
		WillReturnError(pgx.ErrNoRows)

	track, err := repo.FindTrackBySlug(ctx, "nonexistent")
	assert.Error(t, err)
	assert.Nil(t, track)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_ListExams(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()
	trackID := uuid.New()

	now := time.Now()
	rows := pgxmock.NewRows([]string{"id", "track_id", "code", "name", "level", "duration_minutes", "total_questions", "passing_score", "blueprint_url", "is_active", "created_at"}).
		AddRow(uuid.New(), trackID, "JN0-100", "JNCIA-Junos", "JNCIA", 90, 60, 65.0, nil, true, now)

	pool.ExpectQuery(`SELECT .+ FROM exams`).WithArgs(trackID).WillReturnRows(rows)

	exams, err := repo.ListExams(ctx, trackID)
	require.NoError(t, err)
	assert.Len(t, exams, 1)
	assert.Equal(t, "JNCIA-Junos", exams[0].Name)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_FindExamByID(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()
	examID := uuid.New()
	trackID := uuid.New()

	rows := pgxmock.NewRows([]string{"id", "track_id", "code", "name", "level", "duration_minutes", "total_questions", "passing_score", "blueprint_url", "is_active", "created_at"}).
		AddRow(examID, trackID, "JN0-100", "JNCIA-Junos", "JNCIA", 90, 60, 65.0, nil, true, time.Now())

	pool.ExpectQuery(`SELECT .+ FROM exams WHERE id`).WithArgs(examID).WillReturnRows(rows)

	exam, err := repo.FindExamByID(ctx, examID)
	require.NoError(t, err)
	assert.Equal(t, examID, exam.ID)
	assert.Equal(t, domain.Level("JNCIA"), exam.Level)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_FindExamByID_NotFound(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()

	pool.ExpectQuery(`SELECT .+ FROM exams WHERE id`).
		WithArgs(uuid.Nil).
		WillReturnError(pgx.ErrNoRows)

	exam, err := repo.FindExamByID(ctx, uuid.Nil)
	assert.Error(t, err)
	assert.Nil(t, exam)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_ListQuestionIDs(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()
	examID := uuid.New()
	q1, q2 := uuid.New(), uuid.New()

	rows := pgxmock.NewRows([]string{"id"}).AddRow(q1).AddRow(q2)
	pool.ExpectQuery(`SELECT id FROM questions WHERE exam_id`).WithArgs(examID).WillReturnRows(rows)

	ids, err := repo.ListQuestionIDs(ctx, examID)
	require.NoError(t, err)
	assert.Len(t, ids, 2)
	assert.Equal(t, q1, ids[0])
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_ListQuestionIDs_Empty(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()
	examID := uuid.New()

	rows := pgxmock.NewRows([]string{"id"})
	pool.ExpectQuery(`SELECT id FROM questions WHERE exam_id`).WithArgs(examID).WillReturnRows(rows)

	ids, err := repo.ListQuestionIDs(ctx, examID)
	require.NoError(t, err)
	assert.Empty(t, ids)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_GetQuestionsByIDs(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()

	qID := uuid.New()
	refURLs := []string{"https://juniper.net/docs"}
	optionsJSON, _ := json.Marshal([]domain.QuestionOption{
		{ID: "A", Text: "Option A", IsCorrect: true},
		{ID: "B", Text: "Option B", IsCorrect: false},
	})

	rows := pgxmock.NewRows([]string{
		"id", "exam_id", "track_id", "question_type", "difficulty", "bloom_level",
		"body", "options", "explanation", "reference_urls", "blueprint_section",
		"blueprint_weight", "is_active", "created_at", "updated_at",
	}).AddRow(qID, uuid.New(), uuid.New(), "single-choice", 3, "understand",
		"What is BGP?", optionsJSON, "BGP is a routing protocol.",
		refURLs, "bgp", 10, true, time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM questions WHERE id = ANY`).WithArgs([]uuid.UUID{qID}).WillReturnRows(rows)

	questions, err := repo.GetQuestionsByIDs(ctx, []uuid.UUID{qID})
	require.NoError(t, err)
	assert.Len(t, questions, 1)
	assert.Equal(t, qID, questions[0].ID)
	assert.Equal(t, "What is BGP?", questions[0].Body)
	assert.Len(t, questions[0].Options, 2)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_GetQuestionsByIDs_MissingID(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()
	qID := uuid.New()

	// Return empty rows — question not found
	rows := pgxmock.NewRows([]string{
		"id", "exam_id", "track_id", "question_type", "difficulty", "bloom_level",
		"body", "options", "explanation", "reference_urls", "blueprint_section",
		"blueprint_weight", "is_active", "created_at", "updated_at",
	})
	pool.ExpectQuery(`SELECT .+ FROM questions WHERE id = ANY`).WithArgs([]uuid.UUID{qID}).WillReturnRows(rows)

	questions, err := repo.GetQuestionsByIDs(ctx, []uuid.UUID{qID})
	assert.Error(t, err)
	assert.Contains(t, err.Error(), "not found")
	assert.Nil(t, questions)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_FindQuestionByID(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()
	qID := uuid.New()

	optionsJSON, _ := json.Marshal([]domain.QuestionOption{
		{ID: "A", Text: "Correct", IsCorrect: true},
	})

	rows := pgxmock.NewRows([]string{
		"id", "exam_id", "track_id", "question_type", "difficulty", "bloom_level",
		"body", "options", "explanation", "reference_urls", "blueprint_section",
		"blueprint_weight", "is_active", "created_at", "updated_at",
	}).AddRow(qID, uuid.New(), uuid.New(), "single-choice", 2, "remember",
		"Question?", optionsJSON, "Explanation", []string{"url"}, "section", 5, true, time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM questions WHERE id`).WithArgs(qID).WillReturnRows(rows)

	question, err := repo.FindQuestionByID(ctx, qID)
	require.NoError(t, err)
	assert.Equal(t, qID, question.ID)
	assert.Len(t, question.Options, 1)
	assert.True(t, question.Options[0].IsCorrect)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_ListQuestions(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()
	examID := uuid.New()

	optionsJSON, _ := json.Marshal([]domain.QuestionOption{
		{ID: "A", Text: "Answer", IsCorrect: true},
	})

	rows := pgxmock.NewRows([]string{
		"id", "exam_id", "track_id", "question_type", "difficulty", "bloom_level",
		"body", "options", "explanation", "reference_urls", "blueprint_section",
		"blueprint_weight", "is_active", "created_at", "updated_at",
	}).AddRow(uuid.New(), examID, uuid.New(), "single-choice", 1, "remember",
		"Q1?", optionsJSON, "Expl", nil, "s1", 5, true, time.Now(), time.Now()).
		AddRow(uuid.New(), examID, uuid.New(), "single-choice", 3, "apply",
			"Q2?", optionsJSON, "Expl", nil, "s2", 5, true, time.Now(), time.Now())

	pool.ExpectQuery(`SELECT .+ FROM questions WHERE exam_id`).WithArgs(examID).WillReturnRows(rows)

	questions, err := repo.ListQuestions(ctx, examID)
	require.NoError(t, err)
	assert.Len(t, questions, 2)
	assert.NoError(t, pool.ExpectationsWereMet())
}

func TestExamRepository_ListExams_Error(t *testing.T) {
	pool, err := pgxmock.NewPool()
	require.NoError(t, err)
	defer pool.Close()

	repo := NewExamRepository(pool)
	ctx := context.Background()

	pool.ExpectQuery(`SELECT .+ FROM exams`).WithArgs(uuid.Nil).WillReturnError(errors.New("connection refused"))

	exams, err := repo.ListExams(ctx, uuid.Nil)
	assert.Error(t, err)
	assert.Nil(t, exams)
	assert.NoError(t, pool.ExpectationsWereMet())
}
