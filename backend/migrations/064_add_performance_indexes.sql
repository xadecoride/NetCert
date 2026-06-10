-- +goose Up
-- +goose StatementBegin

-- ============================================================
-- Migration 064: Add performance composite indexes
-- ============================================================

-- Speed up history queries: attempts by user + exam
CREATE INDEX IF NOT EXISTS idx_attempts_user_exam ON attempts(user_id, exam_id);

-- Speed up exam question filtering by difficulty
CREATE INDEX IF NOT EXISTS idx_questions_exam_difficulty ON questions(exam_id, difficulty);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP INDEX IF EXISTS idx_attempts_user_exam;
DROP INDEX IF EXISTS idx_questions_exam_difficulty;
-- +goose StatementEnd
