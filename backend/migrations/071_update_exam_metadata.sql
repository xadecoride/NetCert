-- +goose Up
-- +goose StatementBegin

-- ============================================================
-- Migration 071: Align exam metadata with real certification codes
-- ============================================================

-- Update Cisco CCNA metadata to match real 200-301 exam
UPDATE exams
SET code = '200-301',
    name = 'CCNA (200-301) Implementing and Administering Cisco Solutions',
    duration_minutes = 120,
    total_questions = 100,
    passing_score = 82.5,
    blueprint_url = 'https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301-CCNA-v1.1.pdf'
WHERE code = 'CCNA-200-301';

-- Update Juniper JNCIA-Junos to real JN0-106
UPDATE exams
SET code = 'JN0-106',
    name = 'JNCIA-Junos (JN0-106)',
    duration_minutes = 90,
    total_questions = 65,
    passing_score = 60.0,
    blueprint_url = 'https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html'
WHERE code = 'JNCIA-Junos-ENT';

UPDATE exams
SET code = 'JN0-201',
    name = 'JNCIA-Junos Service Provider (JN0-201)',
    duration_minutes = 90,
    total_questions = 65,
    passing_score = 60.0
WHERE code = 'JNCIA-Junos-SP';

UPDATE exams
SET code = 'JN0-230',
    name = 'JNCIA-Security (JN0-230)',
    duration_minutes = 90,
    total_questions = 65,
    passing_score = 60.0
WHERE code = 'JNCSA-Junos';

UPDATE exams
SET code = 'JN0-480',
    name = 'JNCIA-Data Center (JN0-480)',
    duration_minutes = 90,
    total_questions = 65,
    passing_score = 60.0
WHERE code = 'JNCDA-Junos';

UPDATE exams
SET code = 'JN0-223',
    name = 'JNCIA-DevOps (JN0-223)',
    duration_minutes = 90,
    total_questions = 65,
    passing_score = 60.0
WHERE code = 'JNCDA-AUT';

-- Update JNCIP exams to real codes
UPDATE exams
SET code = 'JN0-649',
    name = 'JNCIP-ENT (JN0-649) Enterprise Routing and Switching',
    duration_minutes = 120,
    total_questions = 65,
    passing_score = 70.0,
    blueprint_url = 'https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html'
WHERE code = 'JNCIP-ENT';

UPDATE exams
SET code = 'JN0-663',
    name = 'JNCIP-SP (JN0-663) Service Provider',
    duration_minutes = 120,
    total_questions = 65,
    passing_score = 70.0
WHERE code = 'JNCIP-SP';

UPDATE exams
SET code = 'JN0-636',
    name = 'JNCIP-SEC (JN0-636) Security',
    duration_minutes = 120,
    total_questions = 65,
    passing_score = 70.0
WHERE code = 'JNCIP-SEC';

UPDATE exams
SET code = 'JN0-637',
    name = 'JNCIP-DC (JN0-637) Data Center',
    duration_minutes = 120,
    total_questions = 65,
    passing_score = 70.0
WHERE code = 'JNCIP-DC';

UPDATE exams
SET code = 'JN0-648',
    name = 'JNCIP-AUT (JN0-648) DevOps and Automation',
    duration_minutes = 120,
    total_questions = 65,
    passing_score = 70.0
WHERE code = 'JNCIP-AUT';

-- Update track names/descriptions to match real certification tracks
UPDATE tracks SET name = 'Juniper Enterprise Routing & Switching',
                  description = 'JNCIA-Junos (JN0-106) and JNCIP-ENT (JN0-649)'
WHERE slug = 'junos-ent';

UPDATE tracks SET name = 'Juniper Service Provider',
                  description = 'JNCIA-SP (JN0-201) and JNCIP-SP (JN0-663)'
WHERE slug = 'junos-sp';

UPDATE tracks SET name = 'Juniper Security',
                  description = 'JNCIA-SEC (JN0-230) and JNCIP-SEC (JN0-636)'
WHERE slug = 'junos-sec';

UPDATE tracks SET name = 'Juniper Data Center',
                  description = 'JNCIA-DC (JN0-480) and JNCIP-DC (JN0-637)'
WHERE slug = 'junos-dc';

UPDATE tracks SET name = 'Juniper DevOps & Automation',
                  description = 'JNCIA-DevOps (JN0-223) and JNCIP-AUT (JN0-648)'
WHERE slug = 'junos-aut';

UPDATE tracks SET name = 'Cisco CCNA',
                  description = 'Cisco CCNA (200-301)'
WHERE slug = 'cisco';

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin

-- Restore previous metadata
UPDATE exams SET code = 'CCNA-200-301', name = 'CCNA (200-301)', duration_minutes = 120, total_questions = 102, passing_score = 70.0, blueprint_url = NULL WHERE code = '200-301';
UPDATE exams SET code = 'JNCIA-Junos-ENT', name = 'JNCIA-Junos (Enterprise Routing)', duration_minutes = 90, total_questions = 60, passing_score = 60.0, blueprint_url = NULL WHERE code = 'JN0-106';
UPDATE exams SET code = 'JNCIA-Junos-SP', name = 'JNCIA-Junos (Service Provider)', duration_minutes = 90, total_questions = 60, passing_score = 60.0 WHERE code = 'JN0-201';
UPDATE exams SET code = 'JNCSA-Junos', name = 'JNCSA-Junos (Security)', duration_minutes = 90, total_questions = 60, passing_score = 60.0 WHERE code = 'JN0-230';
UPDATE exams SET code = 'JNCDA-Junos', name = 'JNCDA-Junos (Data Center)', duration_minutes = 90, total_questions = 60, passing_score = 60.0 WHERE code = 'JN0-480';
UPDATE exams SET code = 'JNCDA-AUT', name = 'JNCDA-Junos (DevOps & Automation)', duration_minutes = 90, total_questions = 60, passing_score = 60.0 WHERE code = 'JN0-223';
UPDATE exams SET code = 'JNCIP-ENT', name = 'JNCIP-ENT (Enterprise Routing & Switching)', duration_minutes = 120, total_questions = 75, passing_score = 70.0, blueprint_url = NULL WHERE code = 'JN0-649';
UPDATE exams SET code = 'JNCIP-SP', name = 'JNCIP-SP (Service Provider)', duration_minutes = 120, total_questions = 65, passing_score = 70.0 WHERE code = 'JN0-663';
UPDATE exams SET code = 'JNCIP-SEC', name = 'JNCIP-SEC (Security)', duration_minutes = 120, total_questions = 65, passing_score = 70.0 WHERE code = 'JN0-636';
UPDATE exams SET code = 'JNCIP-DC', name = 'JNCIP-DC (Data Center)', duration_minutes = 120, total_questions = 65, passing_score = 70.0 WHERE code = 'JN0-637';
UPDATE exams SET code = 'JNCIP-AUT', name = 'JNCIP-AUT (DevOps & Automation)', duration_minutes = 120, total_questions = 65, passing_score = 70.0 WHERE code = 'JN0-648';

UPDATE tracks SET name = 'Juniper Enterprise Routing & Switching (ENT)', description = 'JNCIA-JNCIP Enterprise Routing & Switching' WHERE slug = 'junos-ent';
UPDATE tracks SET name = 'Juniper Service Provider (SP)', description = 'JNCIA-JNCIP Service Provider' WHERE slug = 'junos-sp';
UPDATE tracks SET name = 'Juniper Security (SEC)', description = 'JNCIA-JNCIP Security' WHERE slug = 'junos-sec';
UPDATE tracks SET name = 'Juniper Data Center (DC)', description = 'JNCIA-JNCIP Data Center' WHERE slug = 'junos-dc';
UPDATE tracks SET name = 'Juniper DevOps & Automation (AUT)', description = 'JNCIA-JNCIP DevOps & Automation' WHERE slug = 'junos-aut';
UPDATE tracks SET name = 'Cisco CCNA/CCNP', description = 'Cisco CCNA (200-301) & CCNP Enterprise' WHERE slug = 'cisco';

-- +goose StatementEnd
