-- +goose Up
CREATE TABLE IF NOT EXISTS explanations (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    version     INTEGER NOT NULL DEFAULT 1,
    sections    JSONB NOT NULL DEFAULT '[]'::jsonb,
    summary     TEXT NOT NULL DEFAULT '',
    is_active   BOOLEAN NOT NULL DEFAULT TRUE,
    created_at  TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at  TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

-- Trigger to auto-update updated_at on row modification
CREATE OR REPLACE FUNCTION update_explanations_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_explanations_updated_at
    BEFORE UPDATE ON explanations
    FOR EACH ROW
    EXECUTE FUNCTION update_explanations_updated_at();


CREATE INDEX IF NOT EXISTS idx_explanations_question_id ON explanations(question_id);
CREATE INDEX IF NOT EXISTS idx_explanations_question_version ON explanations(question_id, version);

-- +goose Down
DROP TABLE IF EXISTS explanations CASCADE;
