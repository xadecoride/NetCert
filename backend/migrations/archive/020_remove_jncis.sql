-- Migration 020: Remove JNCIS level completely
-- Juniper deprecated the JNCIS level; only JNCIA → JNCIP → JNCIE remain

BEGIN;

-- 1. Delete questions belonging to JNCIS exams
DELETE FROM questions
WHERE exam_id IN (
    SELECT id FROM exams WHERE level = 'JNCIS'
);

-- 2. Delete JNCIS exams
DELETE FROM exams WHERE level = 'JNCIS';

-- 3. Drop old CHECK constraint, recreate without JNCIS
ALTER TABLE exams DROP CONSTRAINT exams_level_check;

ALTER TABLE exams ADD CONSTRAINT exams_level_check
    CHECK (level::text = ANY (ARRAY[
        'JNCIA'::character varying,
        'JNCIP'::character varying,
        'JNCIE'::character varying,
        'CCNA'::character varying,
        'CCNP'::character varying,
        'CCIE'::character varying
    ]::text[]));

COMMIT;
