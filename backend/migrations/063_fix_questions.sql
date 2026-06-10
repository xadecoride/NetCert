-- +goose Up
-- +goose StatementBegin

-- ============================================================
-- Migration 063: Fix corrupted questions and duplicates
-- ============================================================
-- Issues fixed:
--   1. Deactivate questions with empty option text (~320)
--   2. Fix questions where all options have is_correct=true (keep only first)
--   3. Deactivate duplicate body questions within same exam (keep lowest id)

-- 1. Deactivate questions with ANY empty option text.
--    These are unreadable to users because option text is blank.
UPDATE questions
SET is_active = false,
    updated_at = NOW()
WHERE id IN (
    SELECT DISTINCT q.id
    FROM questions q,
         LATERAL jsonb_array_elements(q.options) AS opt
    WHERE q.is_active = true
      AND (opt->>'text' IS NULL OR opt->>'text' = '')
);

-- 2. Fix active questions where ALL options are marked is_correct=true
--    (single-choice must have exactly 1 correct option).
--    Keep is_correct=true only on the first option, set others to false.
UPDATE questions
SET options = (
    SELECT jsonb_agg(
        CASE
            WHEN ord = 1 THEN elem
            ELSE jsonb_set(elem, '{is_correct}', 'false')
        END
        ORDER BY ord
    )
    FROM jsonb_array_elements(options) WITH ORDINALITY AS t(elem, ord)
),
    updated_at = NOW()
WHERE id IN (
    SELECT q.id
    FROM questions q,
         LATERAL jsonb_array_elements(q.options) AS opt
    WHERE q.is_active = true
    GROUP BY q.id
    HAVING COUNT(*) FILTER (WHERE (opt->>'is_correct')::boolean = true) = COUNT(*)
       AND COUNT(*) > 0
);

-- 3. Deactivate duplicate body questions within the same exam (keep lowest id)
UPDATE questions
SET is_active = false,
    updated_at = NOW()
WHERE id IN (
    SELECT q.id
    FROM questions q
    INNER JOIN (
        SELECT exam_id, LOWER(TRIM(body)) AS body_clean,
               (array_agg(id ORDER BY id))[1]::uuid AS keep_id
        FROM questions
        WHERE is_active = true
        GROUP BY exam_id, LOWER(TRIM(body))
        HAVING COUNT(*) > 1
    ) dups ON q.exam_id = dups.exam_id AND LOWER(TRIM(q.body)) = dups.body_clean
    WHERE q.id != dups.keep_id
      AND q.is_active = true
);

-- +goose StatementEnd

-- +goose Down
-- +goose StatementBegin
-- NOTE: Rollback is intentionally best-effort. We re-activate questions
--       that were recently deactivated by this migration. We cannot
--       restore the exact previous state of 'options' arrays.
UPDATE questions
SET is_active = true,
    updated_at = NOW()
WHERE is_active = false
  AND updated_at >= NOW() - INTERVAL '1 hour';
-- +goose StatementEnd
