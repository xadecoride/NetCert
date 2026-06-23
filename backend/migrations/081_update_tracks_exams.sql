-- +goose Up
-- +goose StatementBegin

-- ============================================================
-- Migration 081: Update tracks/exams — CCNA 2.0 rename,
-- restore JNCIS level, add JNCIS exams and JNCIA-Cloud
-- ============================================================

-- 1. Rename CCNA → CCNA 2.0
UPDATE exams
SET code = 'CCNA-2.0',
    name = 'CCNA 2.0'
WHERE id = 'b0000000-0000-0000-0000-000000000003';

UPDATE tracks
SET description = 'Cisco CCNA 2.0 & CCNP Enterprise'
WHERE slug = 'cisco';

-- 2. Restore JNCIS in level check constraints
ALTER TABLE exams DROP CONSTRAINT IF EXISTS exams_level_check;
ALTER TABLE exams ADD CONSTRAINT exams_level_check
  CHECK (level IN ('JNCIA', 'JNCIS', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE'));

ALTER TABLE micro_labs DROP CONSTRAINT IF EXISTS micro_labs_level_check;
ALTER TABLE micro_labs ADD CONSTRAINT micro_labs_level_check
  CHECK (level IN ('JNCIA', 'JNCIS', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE'));

-- 3. Update track descriptions to include JNCIS
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP Enterprise Routing & Switching' WHERE slug = 'junos-ent';
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP Service Provider'             WHERE slug = 'junos-sp';
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP Security'                      WHERE slug = 'junos-sec';
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP Data Center'                   WHERE slug = 'junos-dc';
UPDATE tracks SET description = 'JNCIA-JNCIS-JNCIP DevOps & Automation'           WHERE slug = 'junos-aut';

-- 4. Add Juniper Cloud track
INSERT INTO tracks (id, slug, vendor, name, description, sort_order) VALUES
  ('a0000000-0000-0000-0000-000000000007', 'junos-cloud',
   'juniper', 'Juniper Cloud',
   'JNCIA-JNCIS-JNCIP Cloud', 7)
ON CONFLICT (id) DO NOTHING;

-- 5. Add JNCIS exams for each existing track
INSERT INTO exams (id, track_id, code, name, level, duration_minutes, total_questions, passing_score, is_active) VALUES
  -- JNCIS Enterprise
  ('b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001',
   'JNCIS-ENT', 'JNCIS-ENT (Enterprise Routing & Switching)', 'JNCIS', 90, 65, 65.0, true),
  -- JNCIS Service Provider
  ('b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002',
   'JNCIS-SP', 'JNCIS-SP (Service Provider)', 'JNCIS', 90, 65, 65.0, true),
  -- JNCIS Security
  ('b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000003',
   'JNCIS-SEC', 'JNCIS-SEC (Security)', 'JNCIS', 90, 65, 65.0, true),
  -- JNCIS Data Center
  ('b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000004',
   'JNCIS-DC', 'JNCIS-DC (Data Center)', 'JNCIS', 90, 65, 65.0, true),
  -- JNCIS DevOps & Automation
  ('b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000005',
   'JNCIS-AUT', 'JNCIS-AUT (DevOps & Automation)', 'JNCIS', 90, 65, 65.0, true)
ON CONFLICT (id) DO NOTHING;

-- 6. Add JNCIA-Cloud exam
INSERT INTO exams (id, track_id, code, name, level, duration_minutes, total_questions, passing_score, is_active) VALUES
  ('b0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000007',
   'JNCIA-Cloud', 'JNCIA-Cloud', 'JNCIA', 90, 60, 60.0, true)
ON CONFLICT (id) DO NOTHING;

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

-- Remove JNCIA-Cloud exam and track
DELETE FROM questions WHERE exam_id = 'b0000000-0000-0000-0000-000000000030';
DELETE FROM exams WHERE id = 'b0000000-0000-0000-0000-000000000030';
DELETE FROM tracks WHERE id = 'a0000000-0000-0000-0000-000000000007';

-- Remove JNCIS exams
DELETE FROM questions WHERE exam_id IN (
  'b0000000-0000-0000-0000-000000000012',
  'b0000000-0000-0000-0000-000000000014',
  'b0000000-0000-0000-0000-000000000025',
  'b0000000-0000-0000-0000-000000000027',
  'b0000000-0000-0000-0000-000000000029'
);
DELETE FROM exams WHERE id IN (
  'b0000000-0000-0000-0000-000000000012',
  'b0000000-0000-0000-0000-000000000014',
  'b0000000-0000-0000-0000-000000000025',
  'b0000000-0000-0000-0000-000000000027',
  'b0000000-0000-0000-0000-000000000029'
);

-- Revert track descriptions
UPDATE tracks SET description = 'JNCIA-JNCIP Enterprise Routing & Switching' WHERE slug = 'junos-ent';
UPDATE tracks SET description = 'JNCIA-JNCIP Service Provider'             WHERE slug = 'junos-sp';
UPDATE tracks SET description = 'JNCIA-JNCIP Security'                      WHERE slug = 'junos-sec';
UPDATE tracks SET description = 'JNCIA-JNCIP Data Center'                   WHERE slug = 'junos-dc';
UPDATE tracks SET description = 'JNCIA-JNCIP DevOps & Automation'           WHERE slug = 'junos-aut';

-- Revert CCNA name
UPDATE exams
SET code = 'CCNA-200-301',
    name = 'CCNA (200-301)'
WHERE id = 'b0000000-0000-0000-0000-000000000003';

UPDATE tracks
SET description = 'Cisco CCNA (200-301) & CCNP Enterprise'
WHERE slug = 'cisco';

-- Drop JNCIS from check constraints (revert to 061 state)
ALTER TABLE exams DROP CONSTRAINT IF EXISTS exams_level_check;
ALTER TABLE exams ADD CONSTRAINT exams_level_check
  CHECK (level IN ('JNCIA', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE'));

ALTER TABLE micro_labs DROP CONSTRAINT IF EXISTS micro_labs_level_check;
ALTER TABLE micro_labs ADD CONSTRAINT micro_labs_level_check
  CHECK (level IN ('JNCIA', 'JNCIP', 'JNCIE', 'CCNA', 'CCNP', 'CCIE'));

-- +goose StatementEnd
