-- +goose Up
-- +goose StatementBegin

ALTER TABLE questions ADD COLUMN IF NOT EXISTS body_translations JSONB DEFAULT '{}'::jsonb;
ALTER TABLE questions ADD COLUMN IF NOT EXISTS options_translations JSONB DEFAULT '{}'::jsonb;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

ALTER TABLE questions DROP COLUMN IF EXISTS body_translations;
ALTER TABLE questions DROP COLUMN IF EXISTS options_translations;

-- +goose StatementEnd
