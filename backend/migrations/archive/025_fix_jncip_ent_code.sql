-- Fix JNCIP-ENT exam code: JN0-664 → JN0-650
-- Research confirms JN0-664 is actually JNCIP-SP, JN0-650 is JNCIP-ENT

UPDATE exams SET code = 'JN0-650'
WHERE code = 'JN0-664' AND level = 'JNCIP' AND name = 'JNCIP-ENT';
