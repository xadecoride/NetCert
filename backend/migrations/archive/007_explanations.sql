-- Migration 007: Knowledge Base — Deep-Dive Explanations
-- Создаёт таблицы explanations и explanation_telemetry

-- Таблица объяснений (версионированная)
CREATE TABLE IF NOT EXISTS explanations (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    version INT NOT NULL DEFAULT 1,
    sections JSONB NOT NULL DEFAULT '[]'::jsonb,
    summary TEXT DEFAULT '',
    is_active BOOLEAN NOT NULL DEFAULT true,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_explanations_question ON explanations(question_id);
CREATE INDEX IF NOT EXISTS idx_explanations_active ON explanations(is_active);

COMMENT ON TABLE explanations IS 'Версионированные deep-dive объяснения к вопросам';
COMMENT ON COLUMN explanations.sections IS 'JSONB-массив секций: [{section_type, title, content, is_collapsible, sort_order}]';
COMMENT ON COLUMN explanations.summary IS 'Краткое TL;DR (2-3 предложения)';

-- Таблица телеметрии просмотра объяснений
CREATE TABLE IF NOT EXISTS explanation_telemetry (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    explanation_id UUID REFERENCES explanations(id) ON DELETE SET NULL,
    question_id UUID REFERENCES questions(id) ON DELETE SET NULL,
    session_id UUID NOT NULL DEFAULT gen_random_uuid(),
    event_type VARCHAR(50) NOT NULL,
    section_type VARCHAR(50),
    distractor_option_id VARCHAR(10),
    time_spent_seconds INT NOT NULL DEFAULT 0,
    metadata JSONB DEFAULT '{}'::jsonb,
    created_at TIMESTAMPTZ NOT NULL DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS idx_telemetry_user ON explanation_telemetry(user_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_event ON explanation_telemetry(event_type);
CREATE INDEX IF NOT EXISTS idx_telemetry_question ON explanation_telemetry(question_id);
CREATE INDEX IF NOT EXISTS idx_telemetry_created ON explanation_telemetry(created_at);
CREATE INDEX IF NOT EXISTS idx_telemetry_session ON explanation_telemetry(session_id);

COMMENT ON TABLE explanation_telemetry IS 'Телеметрия взаимодействия пользователя с объяснениями';
COMMENT ON COLUMN explanation_telemetry.event_type IS 'Тип события: explanation_opened, section_expanded, distractor_viewed, code_copied, svg_zoomed, time_spent';
COMMENT ON COLUMN explanation_telemetry.session_id IS 'Идентификатор сессии просмотра (группировка событий одного открытия)';
