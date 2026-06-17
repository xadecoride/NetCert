"""Shared utilities and data structures for NetCert question generators."""
import hashlib
import json
import random
import re
import uuid
from dataclasses import dataclass


@dataclass(frozen=True)
class Exam:
    slug: str
    exam_id: str
    track_id: str
    name: str
    vendor: str
    url: str


@dataclass
class Question:
    id: str
    exam_id: str
    track_id: str
    question_type: str
    difficulty: int
    bloom_level: str
    body: str
    options: list[dict]
    explanation: str
    reference_urls: list[str]
    blueprint_section: str
    blueprint_weight: float
    content_hash: str
    is_active: bool = True


def qid(exam_slug: str, seed: str) -> str:
    return str(uuid.uuid5(uuid.NAMESPACE_OID, f"netcert-v7:{exam_slug}:{seed}"))


def content_hash(body: str, correct: str) -> str:
    return hashlib.sha256(f"{body}::{correct}".encode()).hexdigest()[:16]


def sanitize_body(body: str) -> str:
    return re.sub(r"\s+", " ", body.strip())


def option_id(i: int) -> str:
    return "ABCDEFGHIJ"[i]


def pick_n(pool: list, rng: random.Random, n: int, exclude=None) -> list:
    filtered = [p for p in pool if p != exclude]
    if len(filtered) <= n:
        return list(filtered)
    return rng.sample(filtered, n)


def shuffle_options(options: list[tuple[str, bool]], rng: random.Random) -> tuple[list[tuple[str, bool]], str]:
    shuffled = list(options)
    rng.shuffle(shuffled)
    correct_letters = [option_id(i) for i, (_, c) in enumerate(shuffled) if c]
    return shuffled, ",".join(sorted(correct_letters))


def unique_questions(questions: list[Question]) -> list[Question]:
    seen = set()
    out = []
    for q in questions:
        key = (q.exam_id, q.body.lower())
        if key not in seen:
            seen.add(key)
            out.append(q)
    return out


def make_single_choice(
    exam: Exam,
    body: str,
    options: list[tuple[str, bool]],
    explanation: str,
    section: str,
    weight: float,
    difficulty: int = 2,
    bloom: str = "understand",
) -> Question:
    correct_count = sum(1 for _, c in options if c)
    assert correct_count == 1, f"single-choice must have exactly 1 correct answer: {body}"
    opts = []
    correct_letter = None
    for i, (text, correct) in enumerate(options):
        lid = option_id(i)
        opts.append({"id": lid, "text": text, "is_correct": correct})
        if correct:
            correct_letter = lid
    body = sanitize_body(body)
    correct_text = next(t for t, c in options if c)
    return Question(
        id=qid(exam.slug, body + correct_text),
        exam_id=exam.exam_id,
        track_id=exam.track_id,
        question_type="single-choice",
        difficulty=difficulty,
        bloom_level=bloom,
        body=body,
        options=opts,
        explanation=explanation.strip(),
        reference_urls=[exam.url],
        blueprint_section=section,
        blueprint_weight=weight,
        content_hash=content_hash(body, correct_letter or ""),
    )


def make_multiple_choice(
    exam: Exam,
    body: str,
    options: list[tuple[str, bool]],
    explanation: str,
    section: str,
    weight: float,
    difficulty: int = 3,
    bloom: str = "analyze",
) -> Question:
    correct_count = sum(1 for _, c in options if c)
    assert 2 <= correct_count <= 3, f"multiple-choice must have 2-3 correct answers: {body}"
    opts = []
    correct_letters = []
    for i, (text, correct) in enumerate(options):
        lid = option_id(i)
        opts.append({"id": lid, "text": text, "is_correct": correct})
        if correct:
            correct_letters.append(lid)
    body = sanitize_body(body)
    correct_text = ",".join(t for t, c in options if c)
    return Question(
        id=qid(exam.slug, body + correct_text),
        exam_id=exam.exam_id,
        track_id=exam.track_id,
        question_type="multiple-choice",
        difficulty=difficulty,
        bloom_level=bloom,
        body=body,
        options=opts,
        explanation=explanation.strip(),
        reference_urls=[exam.url],
        blueprint_section=section,
        blueprint_weight=weight,
        content_hash=content_hash(body, "".join(correct_letters)),
    )


def make_fill_blank(
    exam: Exam,
    body: str,
    correct: str,
    options: list[str],
    explanation: str,
    section: str,
    weight: float,
    difficulty: int = 3,
    bloom: str = "apply",
) -> Question:
    body = sanitize_body(body)
    opts = [{"id": option_id(i), "text": text, "is_correct": text == correct} for i, text in enumerate(options)]
    assert sum(1 for o in opts if o["is_correct"]) == 1
    return Question(
        id=qid(exam.slug, body + correct),
        exam_id=exam.exam_id,
        track_id=exam.track_id,
        question_type="fill-blank",
        difficulty=difficulty,
        bloom_level=bloom,
        body=body,
        options=opts,
        explanation=explanation.strip(),
        reference_urls=[exam.url],
        blueprint_section=section,
        blueprint_weight=weight,
        content_hash=content_hash(body, correct),
    )


def make_drag_drop(
    exam: Exam,
    body: str,
    pairs: list[tuple[str, str]],
    explanation: str,
    section: str,
    weight: float,
    difficulty: int = 3,
    bloom: str = "understand",
) -> Question:
    body = sanitize_body(body)
    opts = [{"id": option_id(i), "text": left, "match": right, "is_correct": True} for i, (left, right) in enumerate(pairs)]
    seed = body + "".join(f"{l}={r}" for l, r in pairs)
    return Question(
        id=qid(exam.slug, seed),
        exam_id=exam.exam_id,
        track_id=exam.track_id,
        question_type="drag-drop",
        difficulty=difficulty,
        bloom_level=bloom,
        body=body,
        options=opts,
        explanation=explanation.strip(),
        reference_urls=[exam.url],
        blueprint_section=section,
        blueprint_weight=weight,
        content_hash=content_hash(body, seed),
    )


def make_simlet(
    exam: Exam,
    body: str,
    cli_output: str,
    options: list[tuple[str, bool]],
    explanation: str,
    section: str,
    weight: float,
    difficulty: int = 4,
    bloom: str = "analyze",
) -> Question:
    correct_count = sum(1 for _, c in options if c)
    assert correct_count == 1
    opts = []
    correct_letter = None
    for i, (text, correct) in enumerate(options):
        lid = option_id(i)
        opts.append({"id": lid, "text": text, "is_correct": correct})
        if correct:
            correct_letter = lid
    body = sanitize_body(body)
    full_body = f"{body}\n\n{cli_output.strip()}"
    correct_text = next(t for t, c in options if c)
    return Question(
        id=qid(exam.slug, full_body + correct_text),
        exam_id=exam.exam_id,
        track_id=exam.track_id,
        question_type="simlet",
        difficulty=difficulty,
        bloom_level=bloom,
        body=full_body,
        options=opts,
        explanation=explanation.strip(),
        reference_urls=[exam.url],
        blueprint_section=section,
        blueprint_weight=weight,
        content_hash=content_hash(full_body, correct_letter or ""),
    )


def pg_dollar_quote(s: str) -> str:
    """Escape a string for PostgreSQL dollar-quoting ($$...$$)."""
    # Choose a tag that does not appear in the string.
    tag = ""
    candidate = "$$"
    while candidate in s:
        tag = f"_{tag}_"
        candidate = f"${tag}$"
    return candidate


def question_to_sql(q: Question, idx: int) -> str:
    body_q = pg_dollar_quote(q.body)
    expl_q = pg_dollar_quote(q.explanation)
    section_q = pg_dollar_quote(q.blueprint_section)
    options_json = json.dumps(q.options, ensure_ascii=False)
    options_q = pg_dollar_quote(options_json)
    ref_array = '{"' + '","'.join(q.reference_urls) + '"}'
    ref_q = pg_dollar_quote(ref_array)
    insert = (
        f"INSERT INTO questions (id, exam_id, track_id, question_type, difficulty, bloom_level, body, options, explanation, reference_urls, blueprint_section, blueprint_weight, content_hash, is_active) "
        f"VALUES ('{q.id}', '{q.exam_id}', '{q.track_id}', '{q.question_type}', {q.difficulty}, '{q.bloom_level}', "
        f"{body_q}{q.body}{body_q}::text, {options_q}{options_json}{options_q}::jsonb, "
        f"{expl_q}{q.explanation}{expl_q}::text, {ref_q}{ref_array}{ref_q}::text[], "
        f"{section_q}{q.blueprint_section}{section_q}::text, {q.blueprint_weight}, '{q.content_hash}', {str(q.is_active).lower()}) "
        f"ON CONFLICT (id) DO NOTHING;"
    )
    return "-- +goose StatementBegin\n" + insert + "\n-- +goose StatementEnd"


def questions_to_sql(exam: Exam, questions: list[Question]) -> str:
    lines = [
        "-- +goose Up",
        "-- +goose StatementBegin",
        f"DELETE FROM questions WHERE exam_id = '{exam.exam_id}';",
        "-- +goose StatementEnd",
        "",
    ]
    for i, q in enumerate(questions):
        lines.append(question_to_sql(q, i))
        lines.append("")
    lines.append("-- +goose Down")
    lines.append("-- +goose StatementBegin")
    lines.append(f"DELETE FROM questions WHERE exam_id = '{exam.exam_id}';")
    lines.append("-- +goose StatementEnd")
    return "\n".join(lines)


# Exam metadata
EXAMS = {
    "ccna": Exam(
        slug="ccna",
        exam_id="b0000000-0000-0000-0000-000000000003",
        track_id="a0000000-0000-0000-0000-000000000006",
        name="CCNA 200-301 v1.1",
        vendor="cisco",
        url="https://learningcontent.cisco.com/documents/marketing/exam-topics/200-301-CCNA-v1.1.pdf",
    ),
    "jncia-junos": Exam(
        slug="jncia-junos",
        exam_id="b0000000-0000-0000-0000-000000000001",
        track_id="a0000000-0000-0000-0000-000000000001",
        name="JNCIA-Junos JN0-106",
        vendor="juniper",
        url="https://www.juniper.net/us/en/training/certification/certification-tracks/jncia-junos.html",
    ),
    "jncip-ent": Exam(
        slug="jncip-ent",
        exam_id="b0000000-0000-0000-0000-000000000011",
        track_id="a0000000-0000-0000-0000-000000000001",
        name="JNCIP-ENT",
        vendor="juniper",
        url="https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-ent.html",
    ),
    "jncip-sp": Exam(
        slug="jncip-sp",
        exam_id="b0000000-0000-0000-0000-000000000013",
        track_id="a0000000-0000-0000-0000-000000000002",
        name="JNCIP-SP",
        vendor="juniper",
        url="https://www.juniper.net/us/en/training/certification/certification-tracks/jncip-sp.html",
    ),
}
