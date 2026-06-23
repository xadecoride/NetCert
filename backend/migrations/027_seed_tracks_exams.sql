-- +goose Up
-- Seed tracks and exams needed by migration 028_v6_questions.sql
-- Track UUIDs: a0000000-...-0001 through a0000000-...-0007
-- Exam UUIDs:  b0000000-...-0001 through b0000000-...-0030

-- ─── Tracks ─────────────────────────────────────────────────

INSERT INTO tracks (id, slug, vendor, name, description, sort_order) VALUES
  ('a0000000-0000-0000-0000-000000000001', 'junos-ent',
   'juniper', 'Juniper Enterprise Routing & Switching (ENT)',
   'JNCIA-JNCIS-JNCIP Enterprise Routing & Switching', 1),
  ('a0000000-0000-0000-0000-000000000002', 'junos-sp',
   'juniper', 'Juniper Service Provider (SP)',
   'JNCIA-JNCIS-JNCIP Service Provider', 2),
  ('a0000000-0000-0000-0000-000000000003', 'junos-sec',
   'juniper', 'Juniper Security (SEC)',
   'JNCIA-JNCIS-JNCIP Security', 3),
  ('a0000000-0000-0000-0000-000000000004', 'junos-dc',
   'juniper', 'Juniper Data Center (DC)',
   'JNCIA-JNCIS-JNCIP Data Center', 4),
  ('a0000000-0000-0000-0000-000000000005', 'junos-aut',
   'juniper', 'Juniper DevOps & Automation (AUT)',
   'JNCIA-JNCIS-JNCIP DevOps & Automation', 5),
  ('a0000000-0000-0000-0000-000000000006', 'cisco',
   'cisco', 'Cisco CCNA/CCNP',
   'Cisco CCNA 2.0 & CCNP Enterprise', 6),
  ('a0000000-0000-0000-0000-000000000007', 'junos-cloud',
   'juniper', 'Juniper Cloud',
   'JNCIA-JNCIS-JNCIP Cloud', 7)
ON CONFLICT (id) DO NOTHING;

-- ─── Exams ──────────────────────────────────────────────────
-- Each exam is mapped to its track. Exam suffixes indicate level:
--   -0001..-0003 → JNCIA/CCNA level (foundational)
--   -0020..-0028 → JNCIP level (advanced)

INSERT INTO exams (id, track_id, code, name, level, duration_minutes, total_questions, passing_score, is_active) VALUES
  -- Track 001: Juniper ENT
  ('b0000000-0000-0000-0000-000000000001', 'a0000000-0000-0000-0000-000000000001',
   'JNCIA-Junos-ENT', 'JNCIA-Junos (Enterprise Routing)', 'JNCIA', 90, 60, 60.0, true),
  ('b0000000-0000-0000-0000-000000000012', 'a0000000-0000-0000-0000-000000000001',
   'JNCIS-ENT', 'JNCIS-ENT (Enterprise Routing & Switching)', 'JNCIS', 90, 65, 65.0, true),
  ('b0000000-0000-0000-0000-000000000011', 'a0000000-0000-0000-0000-000000000001',
   'JNCIP-ENT', 'JNCIP-ENT (Enterprise Routing & Switching)', 'JNCIP', 120, 75, 70.0, true),

  -- Track 002: Juniper SP
  ('b0000000-0000-0000-0000-000000000002', 'a0000000-0000-0000-0000-000000000002',
   'JNCIA-Junos-SP', 'JNCIA-Junos (Service Provider)', 'JNCIA', 90, 60, 60.0, true),
  ('b0000000-0000-0000-0000-000000000014', 'a0000000-0000-0000-0000-000000000002',
   'JNCIS-SP', 'JNCIS-SP (Service Provider)', 'JNCIS', 90, 65, 65.0, true),
  ('b0000000-0000-0000-0000-000000000013', 'a0000000-0000-0000-0000-000000000002',
   'JNCIP-SP', 'JNCIP-SP (Service Provider)', 'JNCIP', 120, 70, 70.0, true),

  -- Track 003: Juniper SEC
  ('b0000000-0000-0000-0000-000000000022', 'a0000000-0000-0000-0000-000000000003',
   'JNCSA-Junos', 'JNCSA-Junos (Security)', 'JNCIA', 90, 60, 60.0, true),
  ('b0000000-0000-0000-0000-000000000025', 'a0000000-0000-0000-0000-000000000003',
   'JNCIS-SEC', 'JNCIS-SEC (Security)', 'JNCIS', 90, 65, 65.0, true),
  ('b0000000-0000-0000-0000-000000000024', 'a0000000-0000-0000-0000-000000000003',
   'JNCIP-SEC', 'JNCIP-SEC (Security)', 'JNCIP', 120, 70, 70.0, true),

  -- Track 004: Juniper DC
  ('b0000000-0000-0000-0000-000000000020', 'a0000000-0000-0000-0000-000000000004',
   'JNCDA-Junos', 'JNCDA-Junos (Data Center)', 'JNCIA', 90, 60, 60.0, true),
  ('b0000000-0000-0000-0000-000000000027', 'a0000000-0000-0000-0000-000000000004',
   'JNCIS-DC', 'JNCIS-DC (Data Center)', 'JNCIS', 90, 65, 65.0, true),
  ('b0000000-0000-0000-0000-000000000026', 'a0000000-0000-0000-0000-000000000004',
   'JNCIP-DC', 'JNCIP-DC (Data Center)', 'JNCIP', 120, 70, 70.0, true),

  -- Track 005: Juniper AUT
  ('b0000000-0000-0000-0000-000000000021', 'a0000000-0000-0000-0000-000000000005',
   'JNCDA-AUT', 'JNCDA-Junos (DevOps & Automation)', 'JNCIA', 90, 60, 60.0, true),
  ('b0000000-0000-0000-0000-000000000029', 'a0000000-0000-0000-0000-000000000005',
   'JNCIS-AUT', 'JNCIS-AUT (DevOps & Automation)', 'JNCIS', 90, 65, 65.0, true),
  ('b0000000-0000-0000-0000-000000000028', 'a0000000-0000-0000-0000-000000000005',
   'JNCIP-AUT', 'JNCIP-AUT (DevOps & Automation)', 'JNCIP', 120, 70, 70.0, true),

  -- Track 006: Cisco
  ('b0000000-0000-0000-0000-000000000003', 'a0000000-0000-0000-0000-000000000006',
   'CCNA-2.0', 'CCNA 2.0', 'CCNA', 120, 102, 70.0, true),

  -- Track 007: Juniper Cloud
  ('b0000000-0000-0000-0000-000000000030', 'a0000000-0000-0000-0000-000000000007',
   'JNCIA-Cloud', 'JNCIA-Cloud', 'JNCIA', 90, 60, 60.0, true)
ON CONFLICT (id) DO NOTHING;

-- +goose Down
DELETE FROM questions WHERE exam_id IN (
  'b0000000-0000-0000-0000-000000000001',
  'b0000000-0000-0000-0000-000000000002',
  'b0000000-0000-0000-0000-000000000003',
  'b0000000-0000-0000-0000-000000000011',
  'b0000000-0000-0000-0000-000000000013',
  'b0000000-0000-0000-0000-000000000020',
  'b0000000-0000-0000-0000-000000000021',
  'b0000000-0000-0000-0000-000000000022',
  'b0000000-0000-0000-0000-000000000024',
  'b0000000-0000-0000-0000-000000000026',
  'b0000000-0000-0000-0000-000000000028'
);
DELETE FROM exams WHERE id LIKE 'b0000000-0000-0000-0000-0000000000%';
DELETE FROM tracks WHERE id LIKE 'a0000000-0000-0000-0000-0000000000%';
