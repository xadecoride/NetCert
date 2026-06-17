"""CCNA question generators using content pools."""
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
    CCNA_CABLES,
    CCNA_CATEGORIES,
    CCNA_COMMANDS,
    CCNA_COMPARISONS,
    CCNA_DEVICES,
    CCNA_DRAG_DROP_POOLS,
    CCNA_FILL_BLANK_POOLS,
    CCNA_MULTIPLE_CHOICE_POOLS,
    CCNA_PROTOCOLS,
    CCNA_SCENARIOS,
    CCNA_SECTIONS,
    CCNA_SIMLETS,
    CCNA_TERMS,
    CCNA_WIRELESS,
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
        "What does {term} represent in networking?",
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


def gen_ccna_commands_single(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_COMMANDS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        cmd, desc, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        body = f"What does the command '{cmd}' do?"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = desc.capitalize()
        wrong_pool = [d for _, d, _ in pool if d != desc]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=desc)
        options = [(correct, True)] + [(w.capitalize(), False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["ccna"], body, options,
            f"'{cmd}' {desc}.", section, weight, 2, "understand"
        ))
    return out


def gen_ccna_commands_which(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_COMMANDS)
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 10:
        attempts += 1
        cmd, desc, section_key = rng.choice(pool)
        section, weight = _section_meta(section_key)
        body = f"Which command {desc}?"
        if body in seen_bodies:
            continue
        seen_bodies.add(body)
        correct = cmd
        wrong_pool = [c for c, _, _ in pool if c != cmd]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=cmd)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        out.append(make_single_choice(
            EXAMS["ccna"], body, options,
            f"'{cmd}' {desc}.", section, weight, 2, "apply"
        ))
    return out


def gen_ccna_comparisons_single(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_COMPARISONS)
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
            EXAMS["ccna"], body, options,
            diff, section, weight, 3, "understand"
        ))
    return out


def gen_ccna_scenarios_single(rng: random.Random, count: int) -> list[Question]:
    out = []
    pool = list(CCNA_SCENARIOS)
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


def gen_ccna_protocols(rng: random.Random, count: int) -> list[Question]:
    """Generate questions from structured protocol data: ports, transport, layer."""
    out = []
    pool = list(CCNA_PROTOCOLS)
    seen = set()
    attempts = 0
    templates = [
        ("Which protocol uses {transport} port {port}?", "name", "port"),
        ("What is the default port for {name}?", "port", "port"),
        ("Which transport protocol does {name} use?", "transport", "transport"),
    ]
    while len(out) < count and attempts < count * 20:
        attempts += 1
        name, port, transport, layer, section_key = rng.choice(pool)
        template, correct_attr, wrong_attr = rng.choice(templates)
        body = template.format(name=name, port=port, transport=transport)
        if body in seen:
            continue
        seen.add(body)
        section, weight = _section_meta(section_key)
        if correct_attr == "name":
            correct = name
            wrong_pool = [n for n, _, _, _, _ in pool if n != name]
        elif correct_attr == "port":
            correct = port
            wrong_pool = [p for _, p, _, _, _ in pool if p != port]
        else:
            correct = transport
            wrong_pool = [t for _, _, t, _, _ in pool if t != transport]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=correct)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        explanation = f"{name} uses {transport} port {port}."
        out.append(make_single_choice(
            EXAMS["ccna"], body, options, explanation, section, weight, 2, "remember"
        ))
    return out


def gen_ccna_devices(rng: random.Random, count: int) -> list[Question]:
    """Generate questions about network devices and OSI layers."""
    out = []
    pool = list(CCNA_DEVICES)
    seen = set()
    attempts = 0
    templates = [
        ("At which OSI layer does a {name} primarily operate?", "layer", "layer"),
        ("Which device {function}?", "name", "name"),
        ("What is the primary function of a {name}?", "function", "function"),
    ]
    while len(out) < count and attempts < count * 20:
        attempts += 1
        name, layer, function, section_key = rng.choice(pool)
        template, correct_attr, _ = rng.choice(templates)
        body = template.format(name=name, layer=layer, function=function)
        if body in seen:
            continue
        seen.add(body)
        section, weight = _section_meta(section_key)
        if correct_attr == "name":
            correct = name
            wrong_pool = [n for n, _, _, _ in pool if n != name]
        elif correct_attr == "layer":
            correct = layer
            wrong_pool = list({l for _, l, _, _ in pool if l != layer})
        else:
            correct = function.capitalize()
            wrong_pool = [f.capitalize() for _, _, f, _ in pool if f != function]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=correct)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        explanation = f"{name} operates at {layer} and {function}."
        out.append(make_single_choice(
            EXAMS["ccna"], body, options, explanation, section, weight, 2, "remember"
        ))
    return out


def gen_ccna_cables(rng: random.Random, count: int) -> list[Question]:
    """Generate questions about cabling characteristics."""
    out = []
    pool = list(CCNA_CABLES)
    seen = set()
    attempts = 0
    templates = [
        ("Which cable type supports {speed} at {distance}?", "type", "type"),
        ("What is the maximum distance of {type} at {speed}?", "distance", "distance"),
        ("Which cable category is {category}?", "type", "type"),
    ]
    while len(out) < count and attempts < count * 20:
        attempts += 1
        ctype, speed, distance, category, section_key = rng.choice(pool)
        template, correct_attr, _ = rng.choice(templates)
        body = template.format(type=ctype, speed=speed, distance=distance, category=category)
        if body in seen:
            continue
        seen.add(body)
        section, weight = _section_meta(section_key)
        if correct_attr == "type":
            correct = ctype
            wrong_pool = [t for t, _, _, _, _ in pool if t != ctype]
        elif correct_attr == "distance":
            correct = distance
            wrong_pool = [d for _, _, d, _, _ in pool if d != distance]
        else:
            correct = category
            wrong_pool = [c for _, _, _, c, _ in pool if c != category]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=correct)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        explanation = f"{ctype} supports {speed} up to {distance} and is {category}."
        out.append(make_single_choice(
            EXAMS["ccna"], body, options, explanation, section, weight, 2, "remember"
        ))
    return out


def gen_ccna_wireless(rng: random.Random, count: int) -> list[Question]:
    """Generate questions about wireless standards."""
    out = []
    pool = list(CCNA_WIRELESS)
    seen = set()
    attempts = 0
    templates = [
        ("Which IEEE 802.11 standard operates in the {band} band?", "name", "name"),
        ("What is the maximum data rate of {name}?", "speed", "speed"),
        ("Which Wi-Fi standard {speed} in the {band} band?", "name", "name"),
    ]
    while len(out) < count and attempts < count * 20:
        attempts += 1
        name, band, speed, section_key = rng.choice(pool)
        template, correct_attr, _ = rng.choice(templates)
        body = template.format(name=name, band=band, speed=speed)
        if body in seen:
            continue
        seen.add(body)
        section, weight = _section_meta(section_key)
        if correct_attr == "name":
            correct = name
            wrong_pool = [n for n, _, _, _ in pool if n != name]
        elif correct_attr == "speed":
            correct = speed
            wrong_pool = [s for _, _, s, _ in pool if s != speed]
        else:
            correct = band
            wrong_pool = [b for _, b, _, _ in pool if b != band]
        wrongs = pick_n(wrong_pool, rng, 3, exclude=correct)
        options = [(correct, True)] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        explanation = f"{name} operates in the {band} band with a maximum speed of {speed}."
        out.append(make_single_choice(
            EXAMS["ccna"], body, options, explanation, section, weight, 2, "remember"
        ))
    return out


def gen_ccna_subnetting(rng: random.Random, count: int) -> list[Question]:
    out = []
    networks = ["192.168", "10.0", "172.16", "203.0.113", "198.51.100"]
    seen = set()
    attempts = 0
    while len(out) < count and attempts < count * 20:
        attempts += 1
        network = rng.choice(networks)
        host = rng.randint(1, 240)
        prefix = rng.choice([24, 25, 26, 27, 28, 29, 30])
        block = 2 ** (32 - prefix)
        net_addr = (host // block) * block
        bcast = net_addr + block - 1
        first = net_addr + 1
        last = bcast - 1
        qtype = rng.choice(["first", "last", "bcast", "hosts"])
        key = (network, host, prefix, qtype)
        if key in seen:
            continue
        seen.add(key)
        if qtype == "first":
            body = f"What is the first valid host address in the subnet {network}.{host}/{prefix}?"
            correct = f"{network}.{first}"
            opts = [f"{network}.{net_addr}", f"{network}.{first}", f"{network}.{last}", f"{network}.{bcast}"]
            explanation = f"For /{prefix} the block size is {block}. Network={network}.{net_addr}, first host={network}.{first}."
        elif qtype == "last":
            body = f"What is the last valid host address in the subnet {network}.{host}/{prefix}?"
            correct = f"{network}.{last}"
            opts = [f"{network}.{net_addr}", f"{network}.{first}", f"{network}.{last}", f"{network}.{bcast}"]
            explanation = f"For /{prefix} the block size is {block}. Broadcast={network}.{bcast}, last host={network}.{last}."
        elif qtype == "bcast":
            body = f"What is the broadcast address for the subnet {network}.{host}/{prefix}?"
            correct = f"{network}.{bcast}"
            opts = [f"{network}.{net_addr}", f"{network}.{first}", f"{network}.{last}", f"{network}.{bcast}"]
            explanation = f"For /{prefix} the next network is {network}.{net_addr + block}, so broadcast={network}.{bcast}."
        else:
            hosts = block - 2
            body = f"How many usable host addresses are available in a /{prefix} subnet?"
            correct = str(hosts)
            opts = [str(hosts - 1), str(hosts), str(hosts + 1), str(block)]
            explanation = f"A /{prefix} subnet has {block} total addresses. Subtract network and broadcast to get {hosts} usable hosts."
        rng.shuffle(opts)
        options = [(o, o == correct) for o in opts]
        out.append(make_single_choice(
            EXAMS["ccna"], body, options, explanation,
            "1.0 Network Fundamentals", 20.0, 3, "apply"
        ))
    return out


def gen_ccna_protocols_multiple(rng: random.Random, count: int) -> list[Question]:
    """Multiple-choice questions about groups of protocols."""
    out = []
    pool = list(CCNA_PROTOCOLS)
    templates = [
        ("Which protocols use {transport}? (Choose two or three.)", "transport"),
        ("Which protocols are considered connection-oriented or reliable? (Choose two or three.)", "reliable"),
        ("Which protocols are commonly used for network management? (Choose two or three.)", "mgmt"),
    ]
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 40:
        attempts += 1
        template, mode = rng.choice(templates)
        if mode == "transport":
            transport = rng.choice(["TCP", "UDP"])
            corrects = [n for n, p, t, l, _ in pool if t == transport or (transport == "TCP" and t == "UDP/TCP")]
            if len(corrects) < 2:
                continue
            n_correct = min(rng.choice([2, 3]), len(corrects))
            selected = rng.sample(corrects, n_correct)
            wrong_pool = [n for n, _, t, _, _ in pool if t != transport and t != "UDP/TCP"]
            body = template.format(transport=transport)
        elif mode == "reliable":
            reliable = {"SSH", "FTP", "SFTP", "SMTP", "POP3", "IMAP", "HTTP", "HTTPS", "BGP", "TACACS+", "LDAPS"}
            corrects = [n for n, _, _, _, _ in pool if n in reliable]
            n_correct = min(rng.choice([2, 3]), len(corrects))
            selected = rng.sample(corrects, n_correct)
            wrong_pool = [n for n, _, _, _, _ in pool if n not in reliable]
            body = template
        else:
            mgmt = {"SNMP", "Syslog", "SSH", "NTP", "DNS", "DHCP server", "DHCP client"}
            corrects = [n for n, _, _, _, _ in pool if n in mgmt]
            n_correct = min(rng.choice([2, 3]), len(corrects))
            selected = rng.sample(corrects, n_correct)
            wrong_pool = [n for n, _, _, _, _ in pool if n not in mgmt]
            body = template
        if len(wrong_pool) < 6 - n_correct:
            continue
        if body in seen_bodies:
            # Vary the body slightly by appending a small random detail
            body = body + f" (variant {len(out)})"
            if body in seen_bodies:
                continue
        seen_bodies.add(body)
        wrongs = rng.sample(wrong_pool, 6 - n_correct)
        options = [(c, True) for c in selected] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        section, weight = _section_meta("1.4 TCP/UDP")
        out.append(make_multiple_choice(
            EXAMS["ccna"], body, options,
            f"Correct answers: {', '.join(selected)}.", section, weight, 3, "understand"
        ))
    return out


def gen_ccna_devices_multiple(rng: random.Random, count: int) -> list[Question]:
    """Multiple-choice questions about device OSI layers/functions."""
    out = []
    pool = list(CCNA_DEVICES)
    templates = [
        ("Which devices primarily operate at {layer}? (Choose two or three.)", "layer"),
    ]
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 40:
        attempts += 1
        template, mode = rng.choice(templates)
        layer = rng.choice(list({l for _, l, _, _ in pool}))
        corrects = [n for n, l2, _, _ in pool if l2 == layer]
        if len(corrects) < 2:
            continue
        n_correct = min(rng.choice([2, 3]), len(corrects))
        selected = rng.sample(corrects, n_correct)
        wrong_pool = [n for n, l2, _, _ in pool if l2 != layer]
        if len(wrong_pool) < 6 - n_correct:
            continue
        body = template.format(layer=layer)
        if body in seen_bodies:
            body = body + f" (variant {len(out)})"
            if body in seen_bodies:
                continue
        seen_bodies.add(body)
        wrongs = rng.sample(wrong_pool, 6 - n_correct)
        options = [(c, True) for c in selected] + [(w, False) for w in wrongs]
        options, _ = shuffle_options(options, rng)
        section, weight = _section_meta("1.1 Network Components")
        out.append(make_multiple_choice(
            EXAMS["ccna"], body, options,
            f"Correct answers operate at {layer}: {', '.join(selected)}.", section, weight, 3, "understand"
        ))
    return out


def gen_ccna_categorical_multiple(rng: random.Random, count: int) -> list[Question]:
    """Generate multiple-choice questions by asking which terms belong to a section."""
    out = []
    pool = list(CCNA_TERMS)
    # Group terms by section
    by_section = {}
    for term, _, section_key in pool:
        by_section.setdefault(section_key, []).append(term)
    eligible = [(sk, terms) for sk, terms in by_section.items() if len(terms) >= 4]
    seen_bodies = set()
    attempts = 0
    while len(out) < count and attempts < count * 20:
        attempts += 1
        section_key, terms = rng.choice(eligible)
        if section_key not in CCNA_CATEGORIES:
            continue
        category = CCNA_CATEGORIES[section_key]
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
            EXAMS["ccna"], body, options, explanation, section, weight, 3, "understand"
        ))
    return out


def generate_ccna(total: int = 1000, seed: int = 42) -> list[Question]:
    rng = random.Random(seed)
    questions: list[Question] = []
    questions += gen_ccna_terms_single(rng, 120)
    questions += gen_ccna_terms_definition(rng, 60)
    questions += gen_ccna_protocols(rng, 50)
    questions += gen_ccna_protocols_multiple(rng, 60)
    questions += gen_ccna_devices(rng, 30)
    questions += gen_ccna_devices_multiple(rng, 30)
    questions += gen_ccna_cables(rng, 20)
    questions += gen_ccna_wireless(rng, 20)
    questions += gen_ccna_commands_single(rng, 52)
    questions += gen_ccna_commands_which(rng, 52)
    questions += gen_ccna_comparisons_single(rng, 24)
    questions += gen_ccna_scenarios_single(rng, 49)
    questions += gen_ccna_simlets(rng, 22)
    questions += gen_ccna_drag_drop(rng, 14)
    questions += gen_ccna_fill_blank(rng, 20)
    questions += gen_ccna_multiple_choice(rng, 32)
    questions += gen_ccna_categorical_multiple(rng, 80)
    questions += gen_ccna_subnetting(rng, 120)
    questions = unique_questions(questions)
    if len(questions) > total:
        questions = rng.sample(questions, total)
    # If we still have fewer than requested, add more subnetting
    while len(questions) < total:
        extra = gen_ccna_subnetting(rng, total - len(questions) + 10)
        questions += extra
        questions = unique_questions(questions)
    return questions[:total]
