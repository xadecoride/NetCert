-- +goose Up
-- +goose StatementBegin

-- ============================================================
-- Migration 061: Remove JNCIS and fix exam question counts
-- ============================================================

-- 1. Fix track descriptions (remove JNCIS references)
UPDATE tracks SET description = REPLACE(description, '-JNCIS', '') WHERE description LIKE '%-JNCIS%';
UPDATE tracks SET description = REPLACE(description, 'JNCIA-JNCIS-JNCIP', 'JNCIA-JNCIP') WHERE description LIKE 'JNCIA-JNCIS-JNCIP%';

-- 2. Remove 'JNCIS' from exams.level CHECK constraint
ALTER TABLE exams DROP CONSTRAINT IF EXISTS exams_level_check;
ALTER TABLE exams ADD CONSTRAINT exams_level_check
  CHECK (level IN ('JNCIA', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE'));

-- Update any records that have 'JNCIS' as level (should be none, but just in case)
UPDATE exams SET level = 'JNCIP' WHERE level = 'JNCIS';

-- 3. Remove 'JNCIS' from micro_labs.level CHECK constraint
ALTER TABLE micro_labs DROP CONSTRAINT IF EXISTS micro_labs_level_check;
ALTER TABLE micro_labs ADD CONSTRAINT micro_labs_level_check
  CHECK (level IN ('JNCIA', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE'));

-- Update micro_labs seed data: JNCIS → JNCIP
UPDATE micro_labs SET level = 'JNCIP' WHERE level = 'JNCIS';

-- 4. Fix exam question counts to REALISTIC values (NOT bank size — just how many questions per exam attempt)
-- JNCIA-level: ~60 questions
UPDATE exams SET total_questions = 60 WHERE code = 'JNCIA-Junos-ENT' AND total_questions != 60;
UPDATE exams SET total_questions = 60 WHERE code = 'JNCIA-Junos-SP'  AND total_questions != 60;
UPDATE exams SET total_questions = 60 WHERE code = 'JNCSA-Junos'     AND total_questions != 60;
UPDATE exams SET total_questions = 60 WHERE code = 'JNCDA-Junos'     AND total_questions != 60;
UPDATE exams SET total_questions = 60 WHERE code = 'JNCDA-AUT'       AND total_questions != 60;

-- CCNA: 102 questions
UPDATE exams SET total_questions = 102 WHERE code = 'CCNA-200-301' AND total_questions != 102;

-- JNCIP-level: ~65-75 questions
UPDATE exams SET total_questions = 75 WHERE code = 'JNCIP-ENT' AND total_questions != 75;
UPDATE exams SET total_questions = 65 WHERE code = 'JNCIP-SP'  AND total_questions != 65;
UPDATE exams SET total_questions = 65 WHERE code = 'JNCIP-SEC' AND total_questions != 65;
UPDATE exams SET total_questions = 65 WHERE code = 'JNCIP-DC'  AND total_questions != 65;
UPDATE exams SET total_questions = 65 WHERE code = 'JNCIP-AUT' AND total_questions != 65;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

-- Restore CHECK constraints with JNCIS
ALTER TABLE exams DROP CONSTRAINT IF EXISTS exams_level_check;
ALTER TABLE exams ADD CONSTRAINT exams_level_check
  CHECK (level IN ('JNCIA', 'JNCIS', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE'));

ALTER TABLE micro_labs DROP CONSTRAINT IF EXISTS micro_labs_level_check;
ALTER TABLE micro_labs ADD CONSTRAINT micro_labs_level_check
  CHECK (level IN ('JNCIA', 'JNCIS', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE'));

-- Restore micro_labs levels (referencing specific slugs)
UPDATE micro_labs SET level = 'JNCIP' WHERE slug IN ('ospf-adjacency', 'ebgp-peering');

-- Restore original track descriptions
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP Enterprise Routing & Switching' WHERE slug = 'junos-ent';
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP Service Provider'             WHERE slug = 'junos-sp';
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP Security'                      WHERE slug = 'junos-sec';
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP Data Center'                   WHERE slug = 'junos-dc';
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP DevOps & Automation'           WHERE slug = 'junos-aut';

-- Restore original question counts
UPDATE exams SET total_questions = 3000 WHERE code = 'JNCIA-Junos-ENT';
UPDATE exams SET total_questions = 449  WHERE code = 'JNCIA-Junos-SP';
UPDATE exams SET total_questions = 445  WHERE code = 'JNCSA-Junos';
UPDATE exams SET total_questions = 367  WHERE code = 'JNCDA-Junos';
UPDATE exams SET total_questions = 388  WHERE code = 'JNCDA-AUT';
UPDATE exams SET total_questions = 2000 WHERE code = 'CCNA-200-301';
UPDATE exams SET total_questions = 75  WHERE code = 'JNCIP-ENT';
UPDATE exams SET total_questions = 70  WHERE code = 'JNCIP-SP';
UPDATE exams SET total_questions = 70  WHERE code = 'JNCIP-SEC';
UPDATE exams SET total_questions = 70  WHERE code = 'JNCIP-DC';
UPDATE exams SET total_questions = 70  WHERE code = 'JNCIP-AUT';

-- +goose StatementEnd
