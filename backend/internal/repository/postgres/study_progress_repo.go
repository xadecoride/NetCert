package postgres

import (
	"context"

	"github.com/google/uuid"
	"github.com/netcert/backend/internal/domain"
)

type StudyProgressRepository struct {
	pool DBPool
}

func NewStudyProgressRepository(pool DBPool) *StudyProgressRepository {
	return &StudyProgressRepository{pool: pool}
}

func (r *StudyProgressRepository) ListByUser(ctx context.Context, userID uuid.UUID) ([]domain.StudyProgress, error) {
	rows, err := r.pool.Query(ctx, `SELECT id, user_id, guide_id, completed_at, created_at FROM study_progress WHERE user_id = $1 ORDER BY completed_at DESC`, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var progress []domain.StudyProgress
	for rows.Next() {
		var p domain.StudyProgress
		if err := rows.Scan(&p.ID, &p.UserID, &p.GuideID, &p.CompletedAt, &p.CreatedAt); err != nil {
			return nil, err
		}
		progress = append(progress, p)
	}
	return progress, nil
}

func (r *StudyProgressRepository) Upsert(ctx context.Context, userID uuid.UUID, guideID string, completed bool) error {
	if completed {
		_, err := r.pool.Exec(ctx, `
			INSERT INTO study_progress (id, user_id, guide_id, completed_at, created_at)
			VALUES (uuid_generate_v4(), $1, $2, NOW(), NOW())
			ON CONFLICT (user_id, guide_id) DO UPDATE SET completed_at = NOW()
		`, userID, guideID)
		return err
	}

	_, err := r.pool.Exec(ctx, `DELETE FROM study_progress WHERE user_id = $1 AND guide_id = $2`, userID, guideID)
	return err
}
