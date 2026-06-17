"""JNCIA-Junos question generators using content pools."""
import random

from .common import (
    EXAMS,
    Question,
    make_drag_drop,
    make_fill_blank,
    make_multiple_choice,
    make_simlet,
    make_single_choice,
    pick_n,
    shuffle_options,
    unique_questions,
)
from .junos_pools import (
    JNCIA_CATEGORIES,
    JNCIA_COMMANDS,
    JNCIA_COMPARISONS,
    JNCIA_DRAG_DROP_POOLS,
    JNCIA_FILL_BLANK_POOLS,
    JNCIA_MULTIPLE_CHOICE_POOLS,
    JNCIA_SCENARIOS,
    JNCIA_SECTIONS,
    JNCIA_SIMLETS,
    JNCIA_TERMS,
)


def _section_meta(section_key: str) -> tuple[str, float]:
    return JNCIA_SECTIONS[section_key]


def _same_section_terms(pool, section_key, exclude_term):
    return [t for t, d, sk in pool if sk == section_key and t != exclude_term]


def _same_section_defs(pool, section_key, exclude_def):
    return [d for t, d, sk in pool if sk == section_key and d != exclude_def]


def gen_jncia_terms_single(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_TERMS)
    seen_bodies = set()
    attempts = 0
    templates = [
        "Which term describes {definition}?",
        "What is the term for {definition}?",
        "Select the term that matches the following description: {definition}",
    ]
    while len(out) < count and attempts < count * 10:
        attempts += 1
        term, definition, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        template = rng.choice(templates)
        body = template.format(definition=definition.lower().rstrip("."))
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = term
        wrong_pool = _same_section_terms(pool, section_key, term)
        if len(wrong_pool) < 3:
            wrong_pool = [t for t, _, _ in pool if t != term]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=term)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["jncia-junos"], body, options,
            f"{correct}: {definition}", section, weight, 2, "remember"
        ))
    return out


def gen_jncia_terms_definition(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_TERMS)
    seen_bodies = set()
    attempts = 0
    templates = [
        "What is {term}?",
        "What does {term} represent in Junos?",
        "Which statement best describes {term}?",
    ]
    while len(out) < count and attempts < count * 10:
        attempts += 1
        term, definition, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        template = rng.choice(templates)
        body = template.format(term=term)
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = definition
        wrong_pool = _same_section_defs(pool, section_key, definition)
        if len(wrong_pool) < 3:
            wrong_pool = [d for _, d, _ in pool if d != definition]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=definition)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["jncia-junos"], body, options,
            f"{term}: {definition}", section, weight, 2, "remember"
        ))
    return out


def gen_jncia_commands_single(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_COMMANDS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        cmd, desc, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        body = f"What does the Junos command '{cmd}' do?"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = desc.capitalize()
        wrong_pool = [d for _, d, _ in pool if d != desc]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=desc)
        options = [(correct, True)] + [(w.capitalize(), False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["jncia-junos"], body, options,
            f"'{cmd}' {desc}.", section, weight, 2, "understand"
        ))
    return out


def gen_jncia_commands_which(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_COMMANDS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        cmd, desc, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        body = f"Which Junos command {desc}?"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = cmd
        wrong_pool = [c for c, _, _ in pool if c != cmd]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=cmd)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["jncia-junos"], body, options,
            f"'{cmd}' {desc}.", section, weight, 2, "apply"
        ))
    return out


def gen_jncia_comparisons_single(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_COMPARISONS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        a, b, diff, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        body = f"What is the key difference between {a} and {b}?"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = diff
        wrongs = []
        for x, y, d, _ in pool:
            if (x, y) != (a, b) and (x == a or x == b or y == a or y == b):
                wrongs.append(d)
                if len(wrongs) >= 3:
                    break
        while len(wrongs) < 3:
            _, _, d, _ = rng.choice(pool)
            if d != diff and d not in wrongs:
                wrongs.append(d)
        options = [(correct, True)] + [(w, False) for w in wrongs[:3]]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["jncia-junos"], body, options,
            diff, section, weight, 3, "understand"
        ))
    return out


def gen_jncia_scenarios_single(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_SCENARIOS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        scenario, condition, result, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        body = f"{scenario}\n{condition}\nWhat is the expected result?"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = result
        wrong_pool = [r for _, _, r, _ in pool if r != result]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=result)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["jncia-junos"], body, options,
            f"Given {scenario} and {condition}, the result is: {result}",
            section, weight, 3, "analyze"
        ))
    return out


def gen_jncia_simlets(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_SIMLETS)
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        output, question, options, explanation, section_key = rng.choice(pool)
        if output in seen:
            continue
        seen.add(output)
        section, weight = _section_meta(section_key)
        out.append(make_simlet(
            EXAMS["jncia-junos"], question, output, options, explanation, section, weight, 4, "analyze"
        ))
    return out


def gen_jncia_drag_drop(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_DRAG_DROP_POOLS)
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        section_key, title, pairs = rng.choice(pool)
        if title in seen:
            continue
        seen.add(title)
        section, weight = _section_meta(section_key)
        selected_pairs = pairs if len(pairs) <= 6 else rng.sample(pairs, 6)
        out.append(make_drag_drop(
            EXAMS["jncia-junos"], title, selected_pairs,
            f"Match the items: {title}", section, weight, 3, "understand"
        ))
    return out


def gen_jncia_fill_blank(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_FILL_BLANK_POOLS)
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        section_key, stem, correct, distractors = rng.choice(pool)
        if stem in seen:
            continue
        seen.add(stem)
        section, weight = _section_meta(section_key)
        options = [correct] + distractors
        rng.shuffle(options)
        out.append(make_fill_blank(
            EXAMS["jncia-junos"], stem, correct, options,
            f"The correct completion is '{correct}'.", section, weight, 3, "apply"
        ))
    return out


def gen_jncia_multiple_choice(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_MULTIPLE_CHOICE_POOLS)
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        section_key, body, corrects, wrongs, explanation = rng.choice(pool)
        if body in seen:
            continue
        seen.add(body)
        section, weight = _section_meta(section_key)
        n_correct = rng.choice([2, 3])
        selected_corrects = corrects[:n_correct]
        n_wrong = 6 - n_correct
        selected_wrongs = wrongs[:n_wrong]
        options = [(c, True) for c in selected_corrects] + [(w, False) for w in selected_wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_multiple_choice(
            EXAMS["jncia-junos"], body, options, explanation, section, weight, 3, "analyze"
        ))
    return out


def gen_jncia_categorical_multiple(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(JNCIA_TERMS)
    by_section = {}
    for term, _, section_key in pool:
        by_section.setdefault(section_key, []).append(term)
    eligible = [(sk, terms) for sk, terms in by_section.items() if len(terms) >= 4]
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 20:
        attempts += 1
        section_key, terms = rng.choice(eligible)
        if section_key not in JNCIA_CATEGORIES:
            continue
        category = JNCIA_CATEGORIES[section_key]
        body = f"Which of the following are {category}? (Choose two or three.)"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        n_correct = rng.choice([2, 3])
        corrects = rng.sample(terms, n_correct)
        wrong_pool = [t for t, _, sk in pool if sk != section_key]
        wrongs = rng.sample(wrong_pool, 6 - n_correct)
        options = [(c, True) for c in corrects] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        section, weight = _section_meta(section_key)
        explanation = f"Correct answers are terms related to {category}: {', '.join(corrects)}."
        out.append(make_multiple_choice(
            EXAMS["jncia-junos"], body, options, explanation, section, weight, 3, "understand"
        ))
    return out


def generate_jncia_junos(total: int = 350, seed: int = 42) -> list[Question]:
    rng = random.Random(seed)
    questions: list[Question] = []
    questions += gen_jncia_terms_single(rng, 120)
    questions += gen_jncia_terms_definition(rng, 60)
    questions += gen_jncia_commands_single(rng, 40)
    questions += gen_jncia_commands_which(rng, 40)
    questions += gen_jncia_comparisons_single(rng, 20)
    questions += gen_jncia_scenarios_single(rng, 40)
    questions += gen_jncia_simlets(rng, 20)
    questions += gen_jncia_drag_drop(rng, 20)
    questions += gen_jncia_fill_blank(rng, 30)
    questions += gen_jncia_multiple_choice(rng, 30)
    questions += gen_jncia_categorical_multiple(rng, 40)
    questions = unique_questions(questions)
    if len(questions) > total:
        questions = rng.sample(questions, total)
    while len(questions) < total:
        extra = gen_jncia_terms_single(rng, total - len(questions) + 10)
        questions += extra
        questions = unique_questions(questions)
    return questions[:total]
