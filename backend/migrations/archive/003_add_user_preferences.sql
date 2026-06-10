-- +goose Up
-- +goose StatementBegin
ALTER TABLE users ADD COLUMN IF NOT EXISTS preferences JSONB DEFAULT '{"language":"en","theme":"system","notifications":{"exam_reminders":true,"weekly_report":true,"new_questions":false,"marketing":false}}'::jsonb;
-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
ALTER TABLE users DROP COLUMN IF EXISTS preferences;
-- +goose StatementEnd
