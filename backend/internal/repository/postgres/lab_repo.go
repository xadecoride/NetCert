package postgres

import (
	"context"
	"encoding/json"
	"time"

	"github.com/google/uuid"
	"github.com/jackc/pgx/v5"
	"github.com/netcert/backend/internal/domain"
)

type LabRepository struct {
	pool DBPool
}

func NewLabRepository(pool DBPool) *LabRepository {
	return &LabRepository{pool: pool}
}

func (r *LabRepository) GetByID(ctx context.Context, id uuid.UUID) (*domain.Lab, error) {
	query := `
		SELECT id, track_id, slug, title, description, level,
		       duration_minutes, topology_yaml, task_description,
		       grading_script_path, fault_config, is_troubleshooting,
		       technology, difficulty, lab_directory, is_active, created_at, updated_at
		FROM micro_labs
		WHERE id = $1 AND is_active = true
	`
	lab := &domain.Lab{}
	var faultConfigJSON []byte
	var difficulty int

	err := r.pool.QueryRow(ctx, query, id).Scan(
		&lab.ID, &lab.TrackID, &lab.Slug, &lab.Title, &lab.Description, &lab.Level,
		&lab.DurationMinutes, &lab.TopologyYAML, &lab.TaskDescription,
		&lab.GradingScript, &faultConfigJSON, &lab.IsTroubleshooting,
		&lab.Technology, &difficulty,
		&lab.LabDirectory, &lab.IsActive, &lab.CreatedAt, &lab.UpdatedAt,
	)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}

	// Map difficulty to score fields for backward compatibility
	lab.MaxScore = difficulty * 20
	lab.PassingScore = int(float64(lab.MaxScore) * 0.65)
	lab.NumDevices = difficulty

	if len(faultConfigJSON) > 0 {
		json.Unmarshal(faultConfigJSON, &lab.FaultConfig)
	}

	return lab, nil
}

func (r *LabRepository) GetBySlug(ctx context.Context, slug string) (*domain.Lab, error) {
	query := `
		SELECT id, track_id, slug, title, description, level,
		       duration_minutes, topology_yaml, task_description,
		       grading_script_path, fault_config, is_troubleshooting,
		       technology, difficulty, lab_directory, is_active, created_at, updated_at
		FROM micro_labs
		WHERE slug = $1 AND is_active = true
	`
	lab := &domain.Lab{}
	var faultConfigJSON []byte
	var difficulty int

	err := r.pool.QueryRow(ctx, query, slug).Scan(
		&lab.ID, &lab.TrackID, &lab.Slug, &lab.Title, &lab.Description, &lab.Level,
		&lab.DurationMinutes, &lab.TopologyYAML, &lab.TaskDescription,
		&lab.GradingScript, &faultConfigJSON, &lab.IsTroubleshooting,
		&lab.Technology, &difficulty,
		&lab.LabDirectory, &lab.IsActive, &lab.CreatedAt, &lab.UpdatedAt,
	)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}

	lab.MaxScore = difficulty * 20
	lab.PassingScore = int(float64(lab.MaxScore) * 0.65)
	lab.NumDevices = difficulty

	if len(faultConfigJSON) > 0 {
		json.Unmarshal(faultConfigJSON, &lab.FaultConfig)
	}

	return lab, nil
}

func (r *LabRepository) ListByTrack(ctx context.Context, trackID uuid.UUID) ([]domain.Lab, error) {
	query := `
		SELECT id, track_id, slug, title, description, level,
		       duration_minutes, difficulty, technology, is_troubleshooting, is_active, created_at
		FROM micro_labs
		WHERE track_id = $1 AND is_active = true
		ORDER BY technology, title
	`
	rows, err := r.pool.Query(ctx, query, trackID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var labs []domain.Lab
	for rows.Next() {
		var l domain.Lab
		var difficulty int
		if err := rows.Scan(
			&l.ID, &l.TrackID, &l.Slug, &l.Title, &l.Description, &l.Level,
			&l.DurationMinutes, &difficulty,
			&l.Technology, &l.IsTroubleshooting, &l.IsActive, &l.CreatedAt,
		); err != nil {
			return nil, err
		}
		l.MaxScore = difficulty * 20
		l.PassingScore = int(float64(l.MaxScore) * 0.65)
		l.NumDevices = difficulty
		labs = append(labs, l)
	}
	return labs, nil
}

// CreateSubmission creates a new lab submission.
func (r *LabRepository) CreateSubmission(ctx context.Context, sub *domain.LabSubmission) error {
	query := `
		INSERT INTO lab_submissions (id, lab_id, user_id, status, pod_id, devices,
		                             started_at, time_remaining_seconds, current_score, max_score)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10)
	`
	devicesJSON, err := json.Marshal(sub.Devices)
	if err != nil {
		return err
	}

	_, err = r.pool.Exec(ctx, query,
		sub.ID, sub.LabID, sub.UserID, sub.Status, sub.PodID, devicesJSON,
		sub.StartedAt, sub.TimeRemainingSec, sub.CurrentScore, sub.MaxScore,
	)
	return err
}

// GetSubmission retrieves a lab submission by ID.
func (r *LabRepository) GetSubmission(ctx context.Context, id uuid.UUID) (*domain.LabSubmission, error) {
	query := `
		SELECT id, lab_id, user_id, status, pod_id, devices,
		       started_at, completed_at, time_remaining_seconds,
		       current_score, max_score, snapshot_id, created_at
		FROM lab_submissions
		WHERE id = $1
	`
	sub := &domain.LabSubmission{}
	var devicesJSON []byte

	err := r.pool.QueryRow(ctx, query, id).Scan(
		&sub.ID, &sub.LabID, &sub.UserID, &sub.Status, &sub.PodID, &devicesJSON,
		&sub.StartedAt, &sub.CompletedAt, &sub.TimeRemainingSec,
		&sub.CurrentScore, &sub.MaxScore, &sub.SnapshotID, &sub.CreatedAt,
	)
	if err != nil {
		if err == pgx.ErrNoRows {
			return nil, nil
		}
		return nil, err
	}

	if len(devicesJSON) > 0 {
		json.Unmarshal(devicesJSON, &sub.Devices)
	}

	return sub, nil
}

// UpdateSubmissionStatus updates the status and optional fields of a submission.
func (r *LabRepository) UpdateSubmissionStatus(ctx context.Context, id uuid.UUID, status domain.LabStatus, devices []domain.LabDevice, score int) error {
	query := `
		UPDATE lab_submissions
		SET status = $2, devices = $3, current_score = $4, updated_at = NOW()
		WHERE id = $1
	`
	devicesJSON, err := json.Marshal(devices)
	if err != nil {
		return err
	}
	_, err = r.pool.Exec(ctx, query, id, status, devicesJSON, score)
	return err
}

// SaveLabScore saves grading results for a module.
func (r *LabRepository) SaveLabScore(ctx context.Context, score *domain.LabScore) error {
	query := `
		INSERT INTO lab_scores (id, submission_id, module_number, module_title,
		                        task_score, max_score, scoring_output, is_autograded)
		VALUES ($1, $2, $3, $4, $5, $6, $7, $8)
	`
	scoringJSON, err := json.Marshal(score.ScoringOutput)
	if err != nil {
		return err
	}

	_, err = r.pool.Exec(ctx, query,
		score.ID, score.SubmissionID, score.ModuleNumber, score.ModuleTitle,
		score.TaskScore, score.MaxScore, scoringJSON, score.IsAutoGraded,
	)
	return err
}

// GetLabScores returns all scores for a submission.
func (r *LabRepository) GetLabScores(ctx context.Context, submissionID uuid.UUID) ([]domain.LabScore, error) {
	query := `
		SELECT id, submission_id, module_number, module_title,
		       task_score, max_score, scoring_output, is_autograded, created_at
		FROM lab_scores
		WHERE submission_id = $1
		ORDER BY module_number
	`
	rows, err := r.pool.Query(ctx, query, submissionID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var scores []domain.LabScore
	for rows.Next() {
		var s domain.LabScore
		var scoringJSON []byte
		if err := rows.Scan(
			&s.ID, &s.SubmissionID, &s.ModuleNumber, &s.ModuleTitle,
			&s.TaskScore, &s.MaxScore, &scoringJSON, &s.IsAutoGraded, &s.CreatedAt,
		); err != nil {
			return nil, err
		}
		if len(scoringJSON) > 0 {
			json.Unmarshal(scoringJSON, &s.ScoringOutput)
		}
		scores = append(scores, s)
	}
	return scores, nil
}

// GetActiveSubmissionsByUser returns active submissions for a user.
func (r *LabRepository) GetActiveSubmissionsByUser(ctx context.Context, userID uuid.UUID) ([]domain.LabSubmission, error) {
	query := `
		SELECT id, lab_id, user_id, status, pod_id, devices,
		       started_at, completed_at, time_remaining_seconds,
		       current_score, max_score, snapshot_id, created_at
		FROM lab_submissions
		WHERE user_id = $1 AND status IN ('deploying', 'running', 'paused')
		ORDER BY started_at DESC
	`
	rows, err := r.pool.Query(ctx, query, userID)
	if err != nil {
		return nil, err
	}
	defer rows.Close()

	var subs []domain.LabSubmission
	for rows.Next() {
		var sub domain.LabSubmission
		var devicesJSON []byte
		if err := rows.Scan(
			&sub.ID, &sub.LabID, &sub.UserID, &sub.Status, &sub.PodID, &devicesJSON,
			&sub.StartedAt, &sub.CompletedAt, &sub.TimeRemainingSec,
			&sub.CurrentScore, &sub.MaxScore, &sub.SnapshotID, &sub.CreatedAt,
		); err != nil {
			return nil, err
		}
		if len(devicesJSON) > 0 {
			json.Unmarshal(devicesJSON, &sub.Devices)
		}
		subs = append(subs, sub)
	}
	return subs, nil
}

// CompleteSubmission marks a submission as completed with a final score.
func (r *LabRepository) CompleteSubmission(ctx context.Context, id uuid.UUID, status domain.LabStatus, finalScore int) error {
	now := time.Now()
	query := `
		UPDATE lab_submissions
		SET status = $2, completed_at = $3, current_score = $4, updated_at = NOW()
		WHERE id = $1
	`
	_, err := r.pool.Exec(ctx, query, id, status, now, finalScore)
	return err
}
