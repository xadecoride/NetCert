#!/usr/bin/env python3
"""
Question Bank Auditor — проверяет все 10,204 вопроса на корректность.

Проверки:
  - body не пустой
  - options: >= 2 опции, как минимум 1 correct
  - explanation не пустой
  - difficulty 1-5
  - question_type валидный
  - bloom_level валидный
  - reference_urls — JSON-массив
  - дубликаты body ВНУТРИ одного exam_id
"""

import json
import sys
import os
from collections import defaultdict

try:
    import psycopg2
except ImportError:
    print("INSTALL psycopg2 first: pip install psycopg2-binary")
    sys.exit(1)

DB_CONFIG = os.environ.get("DATABASE_URL", "postgresql://netcert:netcert@localhost:5432/netcert")

VALID_QUESTION_TYPES = {"single-choice", "multiple-choice", "drag-drop", "fill-blank", "simlet", "sim", "lab-task"}
VALID_BLOOM_LEVELS = {"remember", "understand", "apply", "analyze", "troubleshoot", "design"}


def main():
    conn = psycopg2.connect(DB_CONFIG)
    cur = conn.cursor()

    # Fetch all questions
    cur.execute("""
        SELECT q.id, q.exam_id, e.code, e.level, e.name as exam_name,
               q.body, q.options, q.explanation, q.question_type, q.difficulty,
               q.bloom_level, q.reference_urls, q.blueprint_section, q.blueprint_weight
        FROM questions q
        JOIN exams e ON e.id = q.exam_id
        WHERE q.is_active = true
        ORDER BY e.code, q.id
    """)
    rows = cur.fetchall()

    total = len(rows)
    errors = []
    warnings = []
    per_exam = defaultdict(lambda: {"total": 0, "errors": 0, "warnings": 0})
    by_type = defaultdict(int)
    by_difficulty = defaultdict(int)
    by_bloom = defaultdict(int)
    bodies_per_exam = defaultdict(set)

    for row in rows:
        qid, eid, code, level, ename, body, opts_json, explanation, qtype, difficulty, bloom, ref_urls, bp_section, bp_weight = row

        exam_key = f"{code} ({level})"
        per_exam[exam_key]["total"] += 1

        q_errors = []
        q_warnings = []

        # 1. Body check
        if not body or len(body.strip()) < 10:
            q_errors.append(f"body too short ({len(body) if body else 0} chars)")

        # 2. Duplicate body within same exam
        body_clean = body.strip().lower() if body else ""
        if body_clean in bodies_per_exam[exam_key]:
            q_warnings.append(f"duplicate body within exam")
        else:
            bodies_per_exam[exam_key].add(body_clean)

        # 3. Options check
        options = []
        if opts_json:
            try:
                if isinstance(opts_json, str):
                    options = json.loads(opts_json)
                else:
                    options = opts_json
            except json.JSONDecodeError:
                q_errors.append("options: invalid JSON")
        else:
            q_errors.append("options: NULL/empty")

        if len(options) < 2:
            q_errors.append(f"options: only {len(options)} options (need >= 2)")

        correct_count = sum(1 for o in options if o.get("is_correct", False))
        if correct_count == 0:
            q_errors.append("options: no correct answer (is_correct=true not found)")

        # Check for option IDs
        for o in options:
            if not o.get("id"):
                q_warnings.append("option missing 'id' field")
                break
            if not o.get("text"):
                q_warnings.append("option missing 'text' field")
                break

        # 4. Explanation check
        if not explanation or len(explanation.strip()) < 20:
            q_warnings.append(f"explanation too short ({len(explanation) if explanation else 0} chars)")

        # 5. Question type check
        if qtype not in VALID_QUESTION_TYPES:
            q_warnings.append(f"unknown question_type '{qtype}'")
        else:
            by_type[qtype] += 1

            # Validate options format matches question type
            if qtype == "single-choice":
                if correct_count != 1:
                    q_errors.append(f"single-choice: expected exactly 1 correct option, got {correct_count}")
            elif qtype == "fill-blank":
                if correct_count != 1:
                    q_errors.append(f"fill-blank: expected exactly 1 correct option, got {correct_count}")
            elif qtype == "multiple-choice":
                if not (2 <= correct_count <= 3):
                    q_errors.append(f"multiple-choice: expected 2-3 correct options, got {correct_count}")
            elif qtype == "simlet":
                if correct_count != 1:
                    q_errors.append(f"simlet: expected exactly 1 correct option, got {correct_count}")
            elif qtype == "drag-drop":
                if correct_count != len(options):
                    q_errors.append(f"drag-drop: expected all options to be correct (matching pairs), got {correct_count}/{len(options)}")

            # Validate option text plausibility
            for o in options:
                text = str(o.get("text", "")).strip()
                if not text:
                    q_errors.append(f"option '{o.get('id')}' has empty text")
                elif len(text) < 2:
                    # Short option text may be valid for numeric answers, DNS record types, etc.
                    q_warnings.append(f"option '{o.get('id')}' has short text '{text}'; verify it is meaningful")

        # 6. Difficulty check
        if not isinstance(difficulty, int) or difficulty < 1 or difficulty > 5:
            q_warnings.append(f"difficulty {difficulty} out of range [1-5]")
        else:
            by_difficulty[difficulty] += 1

        # 7. Bloom level check
        if bloom and bloom not in VALID_BLOOM_LEVELS:
            q_warnings.append(f"unknown bloom_level '{bloom}'")
        if bloom:
            by_bloom[bloom] += 1

        # 8. Reference URLs check
        if ref_urls:
            try:
                if isinstance(ref_urls, str):
                    urls = json.loads(ref_urls)
                else:
                    urls = ref_urls
                if not isinstance(urls, list):
                    q_warnings.append("reference_urls: not a list")
            except json.JSONDecodeError:
                q_warnings.append("reference_urls: invalid JSON")

        # 9. Blueprint weight (if present)
        if bp_weight is not None and (bp_weight < 0 or bp_weight > 100):
            q_warnings.append(f"blueprint_weight {bp_weight} out of range [0-100]")

        # Collect
        if q_errors:
            errors.append({"id": qid, "exam": exam_key, "issues": q_errors, "body_preview": body[:80] if body else ""})
        if q_warnings:
            warnings.append({"id": qid, "exam": exam_key, "issues": q_warnings, "body_preview": body[:80] if body else ""})

        if q_errors:
            per_exam[exam_key]["errors"] += 1
        if q_warnings:
            per_exam[exam_key]["warnings"] += 1

    cur.close()
    conn.close()

    # ======= REPORT =======
    print("=" * 72)
    print("            QUESTION BANK AUDIT REPORT")
    print("=" * 72)
    print(f"\nTotal questions audited: {total}")

    print("\n" + "-" * 72)
    print("PER-EXAM BREAKDOWN:")
    print("-" * 72)
    for exam_key in sorted(per_exam.keys()):
        stats = per_exam[exam_key]
        status = "✅" if stats["errors"] == 0 and stats["warnings"] == 0 else "⚠️"
        print(f"  {status} {exam_key}: {stats['total']} questions, "
              f"{stats['errors']} errors, {stats['warnings']} warnings")

    print("\n" + "-" * 72)
    print("BY QUESTION TYPE:")
    print("-" * 72)
    for qt, count in sorted(by_type.items(), key=lambda x: -x[1]):
        print(f"  {qt}: {count}")

    print("\n" + "-" * 72)
    print("BY DIFFICULTY:")
    print("-" * 72)
    for d in range(1, 6):
        count = by_difficulty.get(d, 0)
        bar = "█" * (count // 100)
        print(f"  [{d}] {count:5d} {bar}")

    print("\n" + "-" * 72)
    print("BY BLOOM LEVEL:")
    print("-" * 72)
    for bl, count in sorted(by_bloom.items(), key=lambda x: -x[1]):
        bar = "█" * (count // 100)
        print(f"  {bl}: {count:5d} {bar}")

    if errors:
        print("\n" + "=" * 72)
        print(f"❌ ERRORS ({len(errors)}):")
        print("=" * 72)
        for e in errors[:20]:
            print(f"  [{e['exam']}] {', '.join(e['issues'])}")
            print(f"    Body: {e['body_preview']}...")
            print()
        if len(errors) > 20:
            print(f"  ... and {len(errors) - 20} more errors")
    else:
        print("\n✅ NO ERRORS FOUND")

    if warnings:
        print("\n" + "-" * 72)
        print(f"⚠️  WARNINGS ({len(warnings)}):")
        print("-" * 72)
        for w in warnings[:15]:
            print(f"  [{w['exam']}] {', '.join(w['issues'])}")
            print(f"    Body: {w['body_preview']}...")
            print()
        if len(warnings) > 15:
            print(f"  ... and {len(warnings) - 15} more warnings")
    else:
        print("\n✅ NO WARNINGS")

    print("\n" + "=" * 72)
    print("AUDIT COMPLETE")
    print("=" * 72)


if __name__ == "__main__":
    main()
