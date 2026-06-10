-- +goose Up
-- +goose StatementBegin

-- ============================================================
-- Migration 050: Lab Sessions & Results
-- ============================================================
-- Создаёт таблицы для управления сессиями лабораторных работ,
-- автоматической проверки и хранения результатов.
-- Эти таблицы использует Go Lab Orchestrator.

-- Lab submissions (one per user per lab session)
CREATE TABLE IF NOT EXISTS lab_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    lab_id UUID NOT NULL REFERENCES micro_labs(id) ON DELETE CASCADE,
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    status VARCHAR(20) NOT NULL DEFAULT 'pending'
        CHECK (status IN ('pending', 'deploying', 'running', 'paused', 'completed', 'failed', 'timed_out')),
    pod_id VARCHAR(100) NOT NULL,
    -- Device list as JSON array
    devices JSONB NOT NULL DEFAULT '[]'::jsonb,
    started_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    completed_at TIMESTAMPTZ,
    time_remaining_seconds INT NOT NULL DEFAULT 0,
    current_score INT NOT NULL DEFAULT 0,
    max_score INT NOT NULL DEFAULT 100,
    -- Snapshot reference for pause/resume
    snapshot_id VARCHAR(100),
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for lab_submissions
CREATE INDEX IF NOT EXISTS idx_lab_submissions_user_status ON lab_submissions(user_id, status);
CREATE INDEX IF NOT EXISTS idx_lab_submissions_lab_id ON lab_submissions(lab_id);
CREATE INDEX IF NOT EXISTS idx_lab_submissions_pod_id ON lab_submissions(pod_id);
CREATE INDEX IF NOT EXISTS idx_lab_submissions_status ON lab_submissions(status);

-- Lab scores (one per module/task within a submission)
CREATE TABLE IF NOT EXISTS lab_scores (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    submission_id UUID NOT NULL REFERENCES lab_submissions(id) ON DELETE CASCADE,
    module_number INT NOT NULL,
    module_title VARCHAR(200) NOT NULL,
    task_score INT NOT NULL DEFAULT 0,
    max_score INT NOT NULL DEFAULT 100,
    -- Detailed scoring output as JSON array of checks
    scoring_output JSONB NOT NULL DEFAULT '[]'::jsonb,
    is_autograded BOOLEAN NOT NULL DEFAULT FALSE,
    is_manually_reviewed BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Indexes for lab_scores
CREATE INDEX IF NOT EXISTS idx_lab_scores_submission ON lab_scores(submission_id);
CREATE INDEX IF NOT EXISTS idx_lab_scores_autograded ON lab_scores(is_autograded) WHERE is_autograded = TRUE;

-- Trigger function to auto-update updated_at
CREATE OR REPLACE FUNCTION update_lab_submissions_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

DROP TRIGGER IF EXISTS trg_lab_submissions_updated_at ON lab_submissions;
CREATE TRIGGER trg_lab_submissions_updated_at
    BEFORE UPDATE ON lab_submissions
    FOR EACH ROW
    EXECUTE FUNCTION update_lab_submissions_updated_at();

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TRIGGER IF EXISTS trg_lab_submissions_updated_at ON lab_submissions;
DROP FUNCTION IF EXISTS update_lab_submissions_updated_at();
DROP TABLE IF EXISTS lab_scores CASCADE;
DROP TABLE IF EXISTS lab_submissions CASCADE;
-- +goose StatementEnd
