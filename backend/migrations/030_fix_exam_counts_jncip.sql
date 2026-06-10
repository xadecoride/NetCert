-- +goose Up
-- +goose StatementBegin
-- Fix JNCIP exam question counts (the 029 migration expects codes matching 027 seed)
UPDATE exams SET total_questions = 75 WHERE code = 'JNCIP-ENT' AND total_questions != 75;
UPDATE exams SET total_questions = 70 WHERE code = 'JNCIP-SP' AND total_questions != 70;
UPDATE exams SET total_questions = 70 WHERE code = 'JNCIP-SEC' AND total_questions != 70;
UPDATE exams SET total_questions = 70 WHERE code = 'JNCIP-DC' AND total_questions != 70;
UPDATE exams SET total_questions = 70 WHERE code = 'JNCIP-AUT' AND total_questions != 70;
-- +goose StatementEnd
-- +goose Down
-- +goose StatementBegin
UPDATE exams SET total_questions = 500 WHERE code = 'JNCIP-ENT';
UPDATE exams SET total_questions = 500 WHERE code = 'JNCIP-SP';
UPDATE exams SET total_questions = 500 WHERE code = 'JNCIP-SEC';
UPDATE exams SET total_questions = 477 WHERE code = 'JNCIP-DC';
UPDATE exams SET total_questions = 478 WHERE code = 'JNCIP-AUT';
-- +goose StatementEnd
