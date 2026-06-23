package postgres

import (
	"context"
	"encoding/json"
	"fmt"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

type ExamRepository struct {
	pool DBPool
}

func NewExamRepository(pool DBPool) *ExamRepository {
	return &ExamRepository{pool: pool}
}

func (r *ExamRepository) ListTracks(ctx context.Context) ([]domain.Track, error) {
	rows, err := r.pool.Query(ctx, `SELECT id, slug, vendor, name, description, icon_url, sort_order, created_at FROM tracks ORDER BY sort_order`)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var tracks []domain.Track
	for rows.Next() {
		var t domain.Track
		if err := rows.Scan(&t.ID, &t.Slug, &t.Vendor, &t.Name, &t.Description, &t.IconURL, &t.SortOrder, &t.CreatedAt); err != nil {
			return nil, err
		}
		tracks = append(tracks, t)
	}
	return tracks, nil
}

func (r *ExamRepository) FindTrackBySlug(ctx context.Context, slug string) (*domain.Track, error) {
	query := `SELECT id, slug, vendor, name, description, icon_url, sort_order, created_at FROM tracks WHERE slug = $1`
	t := &domain.Track{}
	err := r.pool.QueryRow(ctx, query, slug).Scan(&t.ID, &t.Slug, &t.Vendor, &t.Name, &t.Description, &t.IconURL, &t.SortOrder, &t.CreatedAt)
	if err != nil {
		return nil, err
	}
	return t, nil
}

func (r *ExamRepository) ListExams(ctx context.Context, trackID uuid.UUID) ([]domain.Exam, error) {
	rows, err := r.pool.Query(ctx, `SELECT id, track_id, code, name, level, duration_minutes, total_questions, passing_score, blueprint_url, is_active, created_at FROM exams WHERE track_id = $1 AND is_active = true ORDER BY level, name`, trackID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var exams []domain.Exam
	for rows.Next() {
		var e domain.Exam
		if err := rows.Scan(&e.ID, &e.TrackID, &e.Code, &e.Name, &e.Level, &e.DurationMinutes, &e.TotalQuestions, &e.PassingScore, &e.BlueprintURL, &e.IsActive, &e.CreatedAt); err != nil {
			return nil, err
		}
		exams = append(exams, e)
	}
	return exams, nil
}

func (r *ExamRepository) FindExamByID(ctx context.Context, id uuid.UUID) (*domain.Exam, error) {
	query := `SELECT id, track_id, code, name, level, duration_minutes, total_questions, passing_score, blueprint_url, is_active, created_at FROM exams WHERE id = $1`
	e := &domain.Exam{}
	err := r.pool.QueryRow(ctx, query, id).Scan(&e.ID, &e.TrackID, &e.Code, &e.Name, &e.Level, &e.DurationMinutes, &e.TotalQuestions, &e.PassingScore, &e.BlueprintURL, &e.IsActive, &e.CreatedAt)
	if err != nil {
		return nil, err
	}
	return e, nil
}

func (r *ExamRepository) scanQuestion(scanner interface{ Scan(dest ...interface{}) error }, q *domain.Question) error {
	var refURLs []string
	var optionsJSON []byte
	err := scanner.Scan(&q.ID, &q.ExamID, &q.TrackID, &q.QuestionType, &q.Difficulty, &q.BloomLevel, &q.Body, &optionsJSON, &q.Explanation, &refURLs, &q.BlueprintSection, &q.BlueprintWeight, &q.IsActive, &q.CreatedAt, &q.UpdatedAt)
	if err != nil {
		return err
	}

	if optionsJSON != nil {
		if err := json.Unmarshal(optionsJSON, &q.Options); err != nil {
			return err
		}
	}
	if len(refURLs) > 0 {
		q.ReferenceURLs = refURLs
	}
	return nil
}

func (r *ExamRepository) FindQuestionByID(ctx context.Context, id uuid.UUID) (*domain.Question, error) {
	query := `SELECT id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, created_at, updated_at FROM questions WHERE id = $1`
	q := &domain.Question{}
	if err := r.scanQuestion(r.pool.QueryRow(ctx, query, id), q); err != nil {
		return nil, err
	}
	return q, nil
}

func (r *ExamRepository) ListQuestions(ctx context.Context, examID uuid.UUID) ([]domain.Question, error) {
	rows, err := r.pool.Query(ctx, `SELECT id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, created_at, updated_at FROM questions WHERE exam_id = $1 AND is_active = true ORDER BY difficulty`, examID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var questions []domain.Question
	for rows.Next() {
		var q domain.Question
		if err := r.scanQuestion(rows, &q); err != nil {
			return nil, err
		}
		questions = append(questions, q)
	}
	return questions, nil
}

// ListQuestionIDs returns only the IDs of active questions for an exam (lightweight)
func (r *ExamRepository) ListQuestionIDs(ctx context.Context, examID uuid.UUID) ([]uuid.UUID, error) {
	rows, err := r.pool.Query(ctx, `SELECT id FROM questions WHERE exam_id = $1 AND is_active = true`, examID)
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

// ListQuestionIDsByType returns active question IDs filtered by question_type.
func (r *ExamRepository) ListQuestionIDsByType(ctx context.Context, examID uuid.UUID, questionType string) ([]uuid.UUID, error) {
	rows, err := r.pool.Query(ctx, `SELECT id FROM questions WHERE exam_id = $1 AND question_type = $2 AND is_active = true`, examID, questionType)
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

// GetQuestionsByIDs fetches questions by their IDs preserving input order
// Returns error if any ID is not found (prevents silent data loss)
func (r *ExamRepository) GetQuestionsByIDs(ctx context.Context, ids []uuid.UUID) ([]domain.Question, error) {
	if len(ids) == 0 {
		return nil, nil
	}
	query := `SELECT id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, is_active, created_at, updated_at FROM questions WHERE id = ANY($1)`
	rows, err := r.pool.Query(ctx, query, ids)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	qMap := make(map[string]domain.Question)
	for rows.Next() {
		var q domain.Question
		if err := r.scanQuestion(rows, &q); err != nil {
			return nil, err
		}
		qMap[q.ID.String()] = q
	}

	result := make([]domain.Question, 0, len(ids))
	for _, id := range ids {
		if q, ok := qMap[id.String()]; ok {
			result = append(result, q)
		} else {
			return nil, fmt.Errorf("question %s not found (deleted or inactive)", id)
		}
	}
	return result, nil
}
