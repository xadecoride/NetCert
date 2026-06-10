#!/bin/bash
# Запуск аудита вопросов через psql (без psycopg2)
set -e

cd /home/daniil/NetCert
export PGPASSWORD=netcert
PSQL_CMD="psql -h localhost -U netcert -d netcert -t -A"

echo "================================================================"
echo "            QUESTION BANK AUDIT REPORT"
echo "================================================================"

TOTAL=$($PSQL_CMD -c "SELECT COUNT(*) FROM questions WHERE is_active = true;")
echo ""
echo "Total active questions: $TOTAL"

echo ""
echo "----------------------------------------------------------------"
echo "PER-EXAM BREAKDOWN:"
echo "----------------------------------------------------------------"
$PSQL_CMD -F'|' -c "
SELECT
  e.code || ' (' || e.level || ')' as exam_key,
  COUNT(q.id) as total,
  COUNT(q.id) FILTER (WHERE q.options IS NULL OR q.options::text = 'null' OR q.options::text = '[]') as empty_opts,
  COUNT(q.id) FILTER (WHERE q.body IS NULL OR length(q.body) < 10) as short_body,
  COUNT(q.id) FILTER (WHERE q.explanation IS NULL OR length(q.explanation) < 20) as short_expl
FROM exams e
LEFT JOIN questions q ON q.exam_id = e.id AND q.is_active = true
WHERE e.is_active = true
GROUP BY e.id, e.code, e.level
ORDER BY e.code;
" | while IFS='|' read -r code total empty short_b short_e; do
    [ -z "$code" ] && continue
    status="OK"
    if [ "$empty" -gt 0 ] || [ "$short_b" -gt 0 ]; then status="FAIL"; fi
    echo "  $code: total=$total empty_opts=$empty short_body=$short_b short_expl=$short_e [$status]"
done

echo ""
echo "----------------------------------------------------------------"
echo "QUESTIONS WITH EMPTY/NULL OPTIONS:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT q.id, e.code, substring(q.body from 1 for 80) as body_preview
FROM questions q
JOIN exams e ON e.id = q.exam_id
WHERE q.is_active = true
  AND (q.options IS NULL OR q.options::text = 'null' OR q.options::text = '[]')
ORDER BY e.code, q.id;
" | head -30

echo ""
echo "----------------------------------------------------------------"
echo "QUESTIONS WITH NO CORRECT ANSWER (is_correct=true):"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT q.id, e.code, q.options::text
FROM questions q
JOIN exams e ON e.id = q.exam_id
WHERE q.is_active = true
  AND q.options IS NOT NULL
  AND NOT EXISTS (
    SELECT 1 FROM jsonb_array_elements(q.options) opt
    WHERE (opt->>'is_correct')::boolean = true
  )
ORDER BY e.code, q.id;
" | head -30

echo ""
echo "----------------------------------------------------------------"
echo "QUESTION TYPE DISTRIBUTION:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT question_type, COUNT(*) as count
FROM questions WHERE is_active = true
GROUP BY question_type ORDER BY count DESC;"

echo ""
echo "----------------------------------------------------------------"
echo "DIFFICULTY DISTRIBUTION:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT difficulty, COUNT(*) as count
FROM questions WHERE is_active = true
GROUP BY difficulty ORDER BY difficulty;"

echo ""
echo "----------------------------------------------------------------"
echo "BLOOM LEVEL DISTRIBUTION:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT COALESCE(bloom_level, '(null)') as bloom, COUNT(*) as count
FROM questions WHERE is_active = true
GROUP BY bloom_level ORDER BY count DESC;"

echo ""
echo "----------------------------------------------------------------"
echo "DUPLICATE BODIES WITHIN SAME EXAM:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
WITH norm AS (
  SELECT q.id, e.code, lower(trim(q.body)) as body_norm, COUNT(*) over (partition by e.code, lower(trim(q.body))) as cnt
  FROM questions q
  JOIN exams e ON e.id = q.exam_id
  WHERE q.is_active = true AND length(q.body) > 10
)
SELECT code, body_norm, cnt FROM norm
WHERE cnt > 1
ORDER BY cnt DESC
LIMIT 20;"

echo ""
echo "----------------------------------------------------------------"
echo "INVALID QUESTION TYPES:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT question_type, COUNT(*) FROM questions
WHERE is_active = true
  AND question_type NOT IN ('single-choice', 'multiple-choice', 'drag-drop', 'fill-blank', 'simlet', 'sim', 'lab-task')
GROUP BY question_type;"

echo ""
echo "----------------------------------------------------------------"
echo "INVALID BLOOM LEVELS:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT bloom_level, COUNT(*) FROM questions
WHERE is_active = true
  AND bloom_level IS NOT NULL
  AND bloom_level NOT IN ('remember', 'understand', 'apply', 'analyze', 'troubleshoot', 'design')
GROUP BY bloom_level;"

echo ""
echo "----------------------------------------------------------------"
echo "OUT-OF-RANGE DIFFICULTY:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT difficulty, COUNT(*) FROM questions
WHERE is_active = true
  AND (difficulty < 1 OR difficulty > 5)
GROUP BY difficulty;"

echo ""
echo "----------------------------------------------------------------"
echo "OPTIONS WITHOUT ID/TEXT FIELDS:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT q.id, e.code, jsonb_array_length(q.options) as opt_count
FROM questions q
JOIN exams e ON e.id = q.exam_id
WHERE q.is_active = true
  AND q.options IS NOT NULL
  AND (
    EXISTS (SELECT 1 FROM jsonb_array_elements(q.options) o WHERE o->>'id' IS NULL)
    OR EXISTS (SELECT 1 FROM jsonb_array_elements(q.options) o WHERE o->>'text' IS NULL)
  )
LIMIT 20;"

echo ""
echo "----------------------------------------------------------------"
echo "JNCIS REFERENCES (should be ZERO - level is removed):"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT e.code, COUNT(q.id) as jncis_count
FROM exams e
LEFT JOIN questions q ON q.exam_id = e.id AND q.is_active = true
WHERE e.level = 'JNCIS' OR q.options::text ILIKE '%jncis%'
GROUP BY e.code
ORDER BY jncis_count DESC;"

echo ""
echo "----------------------------------------------------------------"
echo "BLUEPRINT WEIGHT OUT OF RANGE [0-100]:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT COUNT(*) FROM questions
WHERE is_active = true
  AND blueprint_weight IS NOT NULL
  AND (blueprint_weight < 0 OR blueprint_weight > 100);"

echo ""
echo "----------------------------------------------------------------"
echo "REFERENCE URLS NOT JSON ARRAY:"
echo "----------------------------------------------------------------"
$PSQL_CMD -c "
SELECT COUNT(*) FROM questions
WHERE is_active = true
  AND reference_urls IS NOT NULL
  AND array_length(reference_urls, 1) IS NULL
  AND length(reference_urls::text) > 0
  AND reference_urls::text NOT LIKE '{%}';"

echo ""
echo "================================================================"
echo "AUDIT COMPLETE"
echo "================================================================"
