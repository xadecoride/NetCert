-- +goose Up
-- +goose StatementBegin

-- 1. Update exam total_questions to REALISTIC counts matching real exams
-- JNCIA exams: ~60-65 questions
UPDATE exams SET total_questions = 60 WHERE code = 'JN0-106';  -- JNCIA-Junos
UPDATE exams SET total_questions = 60 WHERE code = 'JN0-201';  -- JNCIA-SP
UPDATE exams SET total_questions = 60 WHERE code = 'JN0-230';  -- JNCIA-SEC
UPDATE exams SET total_questions = 60 WHERE code = 'JN0-480';  -- JNCIA-DC
UPDATE exams SET total_questions = 60 WHERE code = 'JN0-223';  -- JNCIA-AUT

-- CCNA: 102 questions (Cisco official)
UPDATE exams SET total_questions = 102 WHERE code = '200-301';

-- JNCIP exams: ~70-75 questions
UPDATE exams SET total_questions = 75 WHERE code = 'JNCIP-ENT';
UPDATE exams SET total_questions = 70 WHERE code = 'JNCIP-SP';
UPDATE exams SET total_questions = 70 WHERE code = 'JNCIP-SEC';
UPDATE exams SET total_questions = 70 WHERE code = 'JNCIP-DC';
UPDATE exams SET total_questions = 70 WHERE code = 'JNCIP-AUT';

-- 2. Create attempt_questions table for storing random subsets
CREATE TABLE attempt_questions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    attempt_id UUID NOT NULL REFERENCES attempts(id) ON DELETE CASCADE,
    question_id UUID NOT NULL REFERENCES questions(id) ON DELETE CASCADE,
    order_index SMALLINT NOT NULL DEFAULT 0,
    UNIQUE(attempt_id, question_id)
);

CREATE INDEX idx_attempt_questions_attempt_id ON attempt_questions(attempt_id);
CREATE INDEX idx_attempt_questions_question_id ON attempt_questions(question_id);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
DROP TABLE IF EXISTS attempt_questions CASCADE;
-- Restore original total_questions (bank sizes)
UPDATE exams SET total_questions = 3000 WHERE code = 'JN0-106';
UPDATE exams SET total_questions = 449 WHERE code = 'JN0-201';
UPDATE exams SET total_questions = 367 WHERE code = 'JN0-230';
UPDATE exams SET total_questions = 388 WHERE code = 'JN0-480';
UPDATE exams SET total_questions = 445 WHERE code = 'JN0-223';
UPDATE exams SET total_questions = 2000 WHERE code = '200-301';
UPDATE exams SET total_questions = 1600 WHERE code = 'JN0-650';
UPDATE exams SET total_questions = 500 WHERE code = 'JNCIP-SP';
UPDATE exams SET total_questions = 500 WHERE code = 'JNCIP-SEC';
UPDATE exams SET total_questions = 477 WHERE code = 'JNCIP-DC';
UPDATE exams SET total_questions = 478 WHERE code = 'JNCIP-AUT';
UPDATE exams SET total_questions = 500 WHERE code = 'JNCIP-ENT';
-- +goose StatementEnd
