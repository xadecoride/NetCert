#!/usr/bin/env python3
"""
NetCert — high-quality, blueprint-aligned question generator v7.
Targets: CCNA 200-301 v1.1, JNCIA-Junos JN0-106, JNCIP-ENT, JNCIP-SP.
Produces single-choice, multiple-choice, drag-drop, fill-blank, and simlet items.
"""
import sys

from generators.ccna import generate_ccna
from generators.common import EXAMS, questions_to_sql
from generators.jncip import generate_jncip_ent, generate_jncip_sp
from generators.junos import generate_jncia_junos


def main():
    exams_to_generate = sys.argv[1:] if len(sys.argv) > 1 else ["ccna", "jncia-junos", "jncip-ent", "jncip-sp"]
    for slug in exams_to_generate:
        if slug == "ccna":
            print("Generating CCNA questions...", file=sys.stderr)
            questions = generate_ccna(total=1000, seed=42)
            filename = "077_ccna_quality_questions.sql"
        elif slug == "jncia-junos":
            print("Generating JNCIA-Junos questions...", file=sys.stderr)
            questions = generate_jncia_junos(total=350, seed=42)
            filename = "078_jncia_junos_quality_questions.sql"
        elif slug == "jncip-ent":
            print("Generating JNCIP-ENT questions...", file=sys.stderr)
            questions = generate_jncip_ent(total=250, seed=42)
            filename = "079_jncip_ent_quality_questions.sql"
        elif slug == "jncip-sp":
            print("Generating JNCIP-SP questions...", file=sys.stderr)
            questions = generate_jncip_sp(total=200, seed=42)
            filename = "080_jncip_sp_quality_questions.sql"
        else:
            print(f"Unknown exam slug: {slug}", file=sys.stderr)
            continue
        print(f"Generated {len(questions)} {slug} questions", file=sys.stderr)
        sql = questions_to_sql(EXAMS[slug], questions)
        with open(f"backend/migrations/{filename}", "w", encoding="utf-8") as f:
            f.write(sql)
        print(f"Wrote backend/migrations/{filename}", file=sys.stderr)


if __name__ == "__main__":
    main()
