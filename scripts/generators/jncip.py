"""JNCIP-ENT and JNCIP-SP question generators using content pools."""
import random

from .common import (
    EXAMS,
    Question,
    make_multiple_choice,
    make_simlet,
    make_single_choice,
    pick_n,
    shuffle_options,
    unique_questions,
)
from .jncip_pools import (
    JNCIP_ENT_COMMANDS,
    JNCIP_ENT_MULTIPLE_CHOICE,
    JNCIP_ENT_SCENARIOS,
    JNCIP_ENT_SECTIONS,
    JNCIP_ENT_SIMLETS,
    JNCIP_ENT_TERMS,
    JNCIP_SP_COMMANDS,
    JNCIP_SP_MULTIPLE_CHOICE,
    JNCIP_SP_SCENARIOS,
    JNCIP_SP_SECTIONS,
    JNCIP_SP_SIMLETS,
    JNCIP_SP_TERMS,
)


def _section_meta(sections, section_key):
    return sections[section_key]


def _same_section_terms(pool, section_key, exclude_term):
    return [t for t, d, sk in pool if sk == section_key and t != exclude_term]


def _same_section_defs(pool, section_key, exclude_def):
    return [d for t, d, sk in pool if sk == section_key and d != exclude_def]


def gen_terms_single(rng, exam, sections, terms, count):
    out = []
    pool = list(terms)
    seen = set()
    attempts = 0
    templates = [
        "Which term describes {definition}?",
        "What is {term}?",
        "Select the term that matches the following description: {definition}",
    ]
    while len(out) < count and attempts < count * 10:
        attempts += 1
        term, definition, section_key = rng.choice(pool)
        section, weight = _section_meta(sections, section_key)
        template = rng.choice(templates)
        if "{term}" in template:
            body = template.format(term=term)
        else:
            body = template.format(definition=definition.lower().rstrip("."))
        if body in seen:
            continue
        seen.add(body)
        if "{term}" in template:
            correct = definition
            wrong_pool = _same_section_defs(pool, section_key, definition)
            if len(wrong_pool) < 3:
                wrong_pool = [d for _, d, _ in pool if d != definition]
        else:
            correct = term
            wrong_pool = _same_section_terms(pool, section_key, term)
            if len(wrong_pool) < 3:
                wrong_pool = [t for t, _, _ in pool if t != term]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=correct)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            exam, body, options, f"{term}: {definition}", section, weight, 3, "remember"
        ))
    return out


def gen_commands(rng, exam, sections, commands, count):
    out = []
    pool = list(commands)
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        cmd, desc, section_key = rng.choice(pool)
        section, weight = _section_meta(sections, section_key)
        if rng.random() < 0.5:
            body = f"What does the Junos command '{cmd}' display?"
            correct = desc.capitalize()
            wrong_pool = [d for _, d, _ in pool if d != desc]
        else:
            body = f"Which Junos command {desc}?"
            correct = cmd
            wrong_pool = [c for c, _, _ in pool if c != cmd]
        if body in seen:
            continue
        seen.add(body)
        wrongs = pick_n(wrong_pool, rng, 3, exclude=correct)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            exam, body, options, f"'{cmd}' {desc}.", section, weight, 3, "understand"
        ))
    return out


def gen_scenarios(rng, exam, sections, scenarios, count):
    out = []
    pool = list(scenarios)
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        scenario, condition, result, section_key = rng.choice(pool)
        section, weight = _section_meta(sections, section_key)
        body = f"{scenario}\n{condition}\nWhat is the expected result?"
        if body in seen:
            continue
        seen.add(body)
        correct = result
        wrong_pool = [r for _, _, r, _ in pool if r != result]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=result)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            exam, body, options,
            f"Given {scenario} and {condition}, the result is: {result}",
            section, weight, 4, "analyze"
        ))
    return out


def gen_simlets(rng, exam, sections, simlets, count):
    out = []
    pool = list(simlets)
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        output, question, options, explanation, section_key = rng.choice(pool)
        if output in seen:
            continue
        seen.add(output)
        section, weight = _section_meta(sections, section_key)
        out.append(make_simlet(exam, question, output, options, explanation, section, weight, 4, "analyze"))
    return out


def gen_multiple_choice(rng, exam, sections, mc_pools, count):
    out = []
    pool = list(mc_pools)
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        section_key, body, corrects, wrongs, explanation = rng.choice(pool)
        if body in seen:
            continue
        seen.add(body)
        section, weight = _section_meta(sections, section_key)
        n_correct = rng.choice([2, 3])
        selected_corrects = corrects[:n_correct]
        selected_wrongs = wrongs[:6 - n_correct]
        options = [(c, True) for c in selected_corrects] + [(w, False) for w in selected_wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_multiple_choice(exam, body, options, explanation, section, weight, 4, "analyze"))
    return out


def generate_jncip_ent(total: int = 250, seed: int = 42) -> list[Question]:
    rng = random.Random(seed)
    questions = []
    questions += gen_terms_single(rng, EXAMS["jncip-ent"], JNCIP_ENT_SECTIONS, JNCIP_ENT_TERMS, 120)
    questions += gen_commands(rng, EXAMS["jncip-ent"], JNCIP_ENT_SECTIONS, JNCIP_ENT_COMMANDS, 60)
    questions += gen_scenarios(rng, EXAMS["jncip-ent"], JNCIP_ENT_SECTIONS, JNCIP_ENT_SCENARIOS, 60)
    questions += gen_simlets(rng, EXAMS["jncip-ent"], JNCIP_ENT_SECTIONS, JNCIP_ENT_SIMLETS, 30)
    questions += gen_multiple_choice(rng, EXAMS["jncip-ent"], JNCIP_ENT_SECTIONS, JNCIP_ENT_MULTIPLE_CHOICE, 60)
    questions = unique_questions(questions)
    if len(questions) > total:
        questions = rng.sample(questions, total)
    while len(questions) < total:
        extra = gen_terms_single(rng, EXAMS["jncip-ent"], JNCIP_ENT_SECTIONS, JNCIP_ENT_TERMS, total - len(questions) + 10)
        questions += extra
        questions = unique_questions(questions)
    return questions[:total]


def generate_jncip_sp(total: int = 200, seed: int = 42) -> list[Question]:
    rng = random.Random(seed)
    questions = []
    questions += gen_terms_single(rng, EXAMS["jncip-sp"], JNCIP_SP_SECTIONS, JNCIP_SP_TERMS, 120)
    questions += gen_commands(rng, EXAMS["jncip-sp"], JNCIP_SP_SECTIONS, JNCIP_SP_COMMANDS, 60)
    questions += gen_scenarios(rng, EXAMS["jncip-sp"], JNCIP_SP_SECTIONS, JNCIP_SP_SCENARIOS, 60)
    questions += gen_simlets(rng, EXAMS["jncip-sp"], JNCIP_SP_SECTIONS, JNCIP_SP_SIMLETS, 30)
    questions += gen_multiple_choice(rng, EXAMS["jncip-sp"], JNCIP_SP_SECTIONS, JNCIP_SP_MULTIPLE_CHOICE, 60)
    questions = unique_questions(questions)
    if len(questions) > total:
        questions = rng.sample(questions, total)
    while len(questions) < total:
        extra = gen_terms_single(rng, EXAMS["jncip-sp"], JNCIP_SP_SECTIONS, JNCIP_SP_TERMS, total - len(questions) + 10)
        questions += extra
        questions = unique_questions(questions)
    return questions[:total]
