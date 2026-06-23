"""CCNA 2.0 question generators using content pools."""
import ipaddress
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
from .ccna_pools import (
    CCNA_CATEGORIES,
    CCNA_COMMANDS,
    CCNA_COMPARISONS,
    CCNA_DRAG_DROP_POOLS,
    CCNA_FILL_BLANK_POOLS,
    CCNA_MULTIPLE_CHOICE_POOLS,
    CCNA_SCENARIOS,
    CCNA_SECTIONS,
    CCNA_SIMLETS,
    CCNA_SUBNETTING_POOLS,
    CCNA_TERMS,
)


def _section_meta(section_key: str) -> tuple[str, float]:
    return CCNA_SECTIONS[section_key]


def _same_section_terms(pool, section_key, exclude_term):
    return [t for t, d, sk in pool if sk == section_key and t != exclude_term]


def _same_section_defs(pool, section_key, exclude_def):
    return [d for t, d, sk in pool if sk == section_key and d != exclude_def]


def gen_ccna_terms_single(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_TERMS)
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
            EXAMS["ccna"], body, options,
            f"{correct}: {definition}", section, weight, 2, "remember"
        ))
    return out


def gen_ccna_terms_definition(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_TERMS)
    seen_bodies = set()
    attempts = 0
    templates = [
        "What is {term}?",
        "What does {term} represent?",
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
            EXAMS["ccna"], body, options,
            f"{term}: {definition}", section, weight, 2, "remember"
        ))
    return out


def gen_ccna_commands(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_COMMANDS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        cmd, desc, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        if rng.random() < 0.5:
            body = f"What does the Cisco IOS command '{cmd}' do?"
            correct = desc.capitalize()
            wrong_pool = [d for _, d, _ in pool if d != desc]
        else:
            body = f"Which command {desc}?"
            correct = cmd
            wrong_pool = [c for c, _, _ in pool if c != cmd]
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        wrongs = pick_n(wrong_pool, rng, 3, exclude=correct)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["ccna"], body, options,
            f"'{cmd}' {desc}.", section, weight, 3, "understand"
        ))
    return out


def gen_ccna_comparisons(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_COMPARISONS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        a, b, diff = rng.choice(pool)
        section_key = rng.choice([
            "1.1 Cable/interface diagnostics",
            "1.2 Virtualization",
            "2.1 Infrastructure connectivity",
            "3.3 OSPF",
            "4.6 ACLs",
            "5.4 SNMP",
        ])
        section, weight = _section_meta(section_key)
        body = f"What is the key difference between {a} and {b}?"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = diff
        wrongs = []
        for x, y, d in pool:
            if (x, y) != (a, b) and (x == a or x == b or y == a or y == b):
                wrongs.append(d)
                if len(wrongs) >= 3:
                    break
        while len(wrongs) < 3:
            _, _, d = rng.choice(pool)
            if d != diff and d not in wrongs:
                wrongs.append(d)
        options = [(correct, True)] + [(w, False) for w in wrongs[:3]]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["ccna"], body, options,
            diff, section, weight, 3, "understand"
        ))
    return out


def gen_ccna_scenarios(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_SCENARIOS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        scenario, condition, result, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        body = f"{scenario}\n{condition}\nWhat is the most likely result or action?"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = result
        wrong_pool = [r for _, _, r, _ in pool if r != result]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=result)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["ccna"], body, options,
            f"Given {scenario} and {condition}, the result is: {result}",
            section, weight, 3, "analyze"
        ))
    return out


def gen_ccna_simlets(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_SIMLETS)
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
            EXAMS["ccna"], question, output, options, explanation, section, weight, 4, "analyze"
        ))
    return out


def gen_ccna_drag_drop(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_DRAG_DROP_POOLS)
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
            EXAMS["ccna"], title, selected_pairs,
            f"Match the items: {title}", section, weight, 3, "understand"
        ))
    return out


def gen_ccna_fill_blank(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_FILL_BLANK_POOLS)
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
            EXAMS["ccna"], stem, correct, options,
            f"The correct completion is '{correct}'.", section, weight, 3, "apply"
        ))
    return out


def gen_ccna_multiple_choice(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_MULTIPLE_CHOICE_POOLS)
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
            EXAMS["ccna"], body, options, explanation, section, weight, 3, "analyze"
        ))
    return out


def _random_ipv4_network(rng: random.Random, mask_len: int | None = None) -> tuple[str, int, str, str, str, str, str]:
    if mask_len is None:
        mask_len = rng.choice([24, 25, 26, 27, 28, 30])
    network_int = rng.randint(0x0A000000, 0x0AFFFFFF) & (0xFFFFFFFF << (32 - mask_len))
    network = ipaddress.IPv4Network((network_int, mask_len), strict=False)
    hosts = list(network.hosts())
    if not hosts:
        return _random_ipv4_network(rng, mask_len)
    ip = str(rng.choice(hosts))
    first = str(hosts[0])
    last = str(hosts[-1])
    broadcast = str(network.broadcast_address)
    num_hosts = len(hosts)
    return ip, mask_len, str(network.network_address), broadcast, first, last, str(num_hosts)


def _random_ipv6_network(rng: random.Random) -> tuple[str, int, int, str]:
    prefix_len = rng.choice([48, 56, 60, 64])
    sub_prefix_len = rng.choice([72, 80, 96])
    if sub_prefix_len <= prefix_len:
        sub_prefix_len = prefix_len + 8
    network = ipaddress.IPv6Network((rng.getrandbits(128), prefix_len), strict=False)
    num_subnets = 2 ** (sub_prefix_len - prefix_len)
    return str(network.network_address), prefix_len, sub_prefix_len, str(num_subnets)


def gen_ccna_subnetting(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_SUBNETTING_POOLS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 20:
        attempts += 1
        template = rng.choice(pool)
        section_key = template["section_key"]
        section, weight = _section_meta(section_key)
        answer_type = template["answer_type"]
        if answer_type == "ipv6_subnets":
            network, prefix_len, sub_prefix_len, num_subnets = _random_ipv6_network(rng)
            body = template["question"].format(ipv6_network=network, prefix_len=prefix_len, sub_prefix_len=sub_prefix_len)
            correct = num_subnets
            explanation = f"A /{prefix_len} prefix can be split into /{sub_prefix_len} subnets: 2^({sub_prefix_len}-{prefix_len}) = {num_subnets}."
        else:
            ip, mask_len, network, broadcast, first, last, num_hosts = _random_ipv4_network(rng)
            body = template["question"].format(ip=ip, mask_len=mask_len, network=network)
            if answer_type == "network":
                correct = network
                explanation = f"The network address for {ip}/{mask_len} is {network}."
            elif answer_type == "broadcast":
                correct = broadcast
                explanation = f"The broadcast address for {network}/{mask_len} is {broadcast}."
            elif answer_type == "hosts":
                correct = num_hosts
                explanation = f"A /{mask_len} subnet has 2^(32-{mask_len}) - 2 = {num_hosts} usable hosts."
            elif answer_type == "last_host":
                correct = last
                explanation = f"The last usable host in {network}/{mask_len} is {last}."
            else:
                continue
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        distractors = []
        if answer_type in ("network", "broadcast", "last_host"):
            for _ in range(10):
                _, ml, net, brc, first2, last2, _ = _random_ipv4_network(rng, mask_len)
                val = {"network": net, "broadcast": brc, "last_host": last2}.get(answer_type, first2)
                if val != correct and val not in distractors:
                    distractors.append(val)
        elif answer_type == "hosts":
            for m in [24, 25, 26, 27, 28, 29, 30]:
                if m != mask_len:
                    h = (1 << (32 - m)) - 2
                    if h > 0 and str(h) != correct and str(h) not in distractors:
                        distractors.append(str(h))
        else:
            for delta in [2, 4, 8, 16, 32]:
                try:
                    val = int(correct) * delta
                    if str(val) != str(correct) and str(val) not in distractors:
                        distractors.append(str(val))
                except ValueError:
                    pass
        options = [(str(correct), True)] + [(str(d), False) for d in distractors[:5]]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["ccna"], body, options,
            explanation, section, weight, 3, "apply"
        ))
    return out


def gen_ccna_categorical_multiple(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_TERMS)
    by_section = {}
    for term, _, section_key in pool:
        by_section.setdefault(section_key, []).append(term)
    eligible = [(sk, terms) for sk, terms in by_section.items() if len(terms) >= 4]
    templates = [
        "Which of the following are {category}? (Choose {n}.)",
        "Select the items that are {category}. (Choose {n}.)",
        "Which terms describe {category}? (Choose {n}.)",
        "Choose the {category} items from the list. (Choose {n}.)",
        "Which statements are true for {category}? (Choose {n} terms.)",
        "Identify the {category}. (Choose {n}.)",
        "Pick the {category} from the options. (Choose {n}.)",
        "Which options represent {category}? (Choose {n}.)",
    ]
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 100:
        attempts += 1
        section_key, terms = rng.choice(eligible)
        if section_key not in CCNA_CATEGORIES:
            continue
        category = CCNA_CATEGORIES[section_key]
        n_correct = rng.choice([2, 3])
        n_text = "two" if n_correct == 2 else "three"
        template = rng.choice(templates)
        body = template.format(category=category, n=n_text)
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        corrects = rng.sample(terms, n_correct)
        wrong_pool = [t for t, _, sk in pool if sk != section_key]
        wrongs = rng.sample(wrong_pool, 6 - n_correct)
        options = [(c, True) for c in corrects] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        section, weight = _section_meta(section_key)
        explanation = f"Correct answers are terms related to {category}: {', '.join(corrects)}."
        out.append(make_multiple_choice(
            EXAMS["ccna"], body, options, explanation, section, weight, 3, "understand"
        ))
    return out


def generate_ccna(total: int = 1000, seed: int = 42) -> list[Question]:
    rng = random.Random(seed)
    questions: list[Question] = []
    questions += gen_ccna_terms_single(rng, 200)
    questions += gen_ccna_terms_definition(rng, 150)
    questions += gen_ccna_commands(rng, 62)
    questions += gen_ccna_comparisons(rng, 15)
    questions += gen_ccna_scenarios(rng, 61)
    questions += gen_ccna_simlets(rng, 8)
    questions += gen_ccna_drag_drop(rng, 9)
    questions += gen_ccna_fill_blank(rng, 22)
    questions += gen_ccna_multiple_choice(rng, 27)
    questions += gen_ccna_categorical_multiple(rng, 400)
    questions += gen_ccna_subnetting(rng, 80)
    questions = unique_questions(questions)
    if len(questions) > total:
        questions = rng.sample(questions, total)
    while len(questions) < total:
        extra = gen_ccna_scenarios(rng, total - len(questions) + 10)
        questions += extra
        questions = unique_questions(questions)
    return questions[:total]
