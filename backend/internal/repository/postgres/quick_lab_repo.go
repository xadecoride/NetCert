package postgres

import (
	"context"
	"encoding/json"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/netcert/backend/internal/domain"
)

type QuickLabRepository struct {
	pool DBPool
}

func NewQuickLabRepository(pool DBPool) *QuickLabRepository {
	return &QuickLabRepository{pool: pool}
}

func (r *QuickLabRepository) GetByID(ctx context.Context, id uuid.UUID) (*domain.QuickLab, error) {
	query := `
		SELECT id, track_id, slug, title, description, level, difficulty,
		       estimated_minutes, technology, topology_svg, pnetlab_instructions,
		       tasks, hints, answers, explanations, solution_commands,
		       prerequisite_topics, is_active, created_at, updated_at
		FROM quick_labs
		WHERE id = $1 AND is_active = true
	`
	ql := &domain.QuickLab{}
	var tasksJSON, hintsJSON, answersJSON, explanationsJSON, solutionJSON []byte
	var prereqTopics []string

	err := r.pool.QueryRow(ctx, query, id).Scan(
		&ql.ID, &ql.TrackID, &ql.Slug, &ql.Title, &ql.Description, &ql.Level, &ql.Difficulty,
		&ql.EstimatedMinutes, &ql.Technology, &ql.TopologySVG, &ql.PnetlabInstructions,
		&tasksJSON, &hintsJSON, &answersJSON, &explanationsJSON, &solutionJSON,
		&prereqTopics, &ql.IsActive, &ql.CreatedAt, &ql.UpdatedAt,
	)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}

	r.unmarshalJSON(tasksJSON, &ql.Tasks)
	r.unmarshalJSON(hintsJSON, &ql.Hints)
	r.unmarshalJSON(answersJSON, &ql.Answers)
	r.unmarshalJSON(explanationsJSON, &ql.Explanations)
	r.unmarshalJSON(solutionJSON, &ql.SolutionCommands)
	ql.PrerequisiteTopics = prereqTopics

	return ql, nil
}

func (r *QuickLabRepository) GetBySlug(ctx context.Context, slug string) (*domain.QuickLab, error) {
	query := `
		SELECT id, track_id, slug, title, description, level, difficulty,
		       estimated_minutes, technology, topology_svg, pnetlab_instructions,
		       tasks, hints, answers, explanations, solution_commands,
		       prerequisite_topics, is_active, created_at, updated_at
		FROM quick_labs
		WHERE slug = $1 AND is_active = true
	`
	ql := &domain.QuickLab{}
	var tasksJSON, hintsJSON, answersJSON, explanationsJSON, solutionJSON []byte
	var prereqTopics []string

	err := r.pool.QueryRow(ctx, query, slug).Scan(
		&ql.ID, &ql.TrackID, &ql.Slug, &ql.Title, &ql.Description, &ql.Level, &ql.Difficulty,
		&ql.EstimatedMinutes, &ql.Technology, &ql.TopologySVG, &ql.PnetlabInstructions,
		&tasksJSON, &hintsJSON, &answersJSON, &explanationsJSON, &solutionJSON,
		&prereqTopics, &ql.IsActive, &ql.CreatedAt, &ql.UpdatedAt,
	)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}

	r.unmarshalJSON(tasksJSON, &ql.Tasks)
	r.unmarshalJSON(hintsJSON, &ql.Hints)
	r.unmarshalJSON(answersJSON, &ql.Answers)
	r.unmarshalJSON(explanationsJSON, &ql.Explanations)
	r.unmarshalJSON(solutionJSON, &ql.SolutionCommands)
	ql.PrerequisiteTopics = prereqTopics

	return ql, nil
}

func (r *QuickLabRepository) ListByTrack(ctx context.Context, trackID uuid.UUID) ([]domain.QuickLab, error) {
	query := `
		SELECT id, track_id, slug, title, description, level, difficulty,
		       estimated_minutes, technology, is_active, created_at
		FROM quick_labs
		WHERE track_id = $1 AND is_active = true
		ORDER BY difficulty, title
	`
	rows, err := r.pool.Query(ctx, query, trackID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var labs []domain.QuickLab
	for rows.Next() {
		var ql domain.QuickLab
		if err := rows.Scan(
			&ql.ID, &ql.TrackID, &ql.Slug, &ql.Title, &ql.Description, &ql.Level, &ql.Difficulty,
			&ql.EstimatedMinutes, &ql.Technology, &ql.IsActive, &ql.CreatedAt,
		); err != nil {
			return nil, err
		}
		labs = append(labs, ql)
	}
	return labs, nil
}

func (r *QuickLabRepository) ListAll(ctx context.Context) ([]domain.QuickLab, error) {
	query := `
		SELECT id, track_id, slug, title, description, level, difficulty,
		       estimated_minutes, technology, is_active, created_at
		FROM quick_labs
		WHERE is_active = true
		ORDER BY difficulty, title
	`
	rows, err := r.pool.Query(ctx, query)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var labs []domain.QuickLab
	for rows.Next() {
		var ql domain.QuickLab
		if err := rows.Scan(
			&ql.ID, &ql.TrackID, &ql.Slug, &ql.Title, &ql.Description, &ql.Level, &ql.Difficulty,
			&ql.EstimatedMinutes, &ql.Technology, &ql.IsActive, &ql.CreatedAt,
		); err != nil {
			return nil, err
		}
		labs = append(labs, ql)
	}
	return labs, nil
}

func (r *QuickLabRepository) unmarshalJSON(data []byte, v interface{}) {
	if len(data) > 0 {
		json.Unmarshal(data, v)
	}
}
