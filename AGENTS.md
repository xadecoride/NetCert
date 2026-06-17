# NetCert — Agent Instructions

## Project overview

NetCert is a certification practice platform with a Go backend, Next.js frontend, and PostgreSQL database. Question banks are managed through `goose` SQL migrations in `backend/migrations/`.

## Question generation

High-quality, blueprint-aligned questions are generated from content pools by Python scripts in `scripts/generators/`.

### Supported exams

| Exam code | Track | Generator | Migration file |
|-----------|-------|-----------|----------------|
| `200-301` | CCNA | `generators.ccna:generate_ccna` | `077_ccna_quality_questions.sql` |
| `JN0-106` | JNCIA-Junos | `generators.junos:generate_jncia_junos` | `078_jncia_junos_quality_questions.sql` |
| `JN0-649` | JNCIP-ENT | `generators.jncip:generate_jncip_ent` | `079_jncip_ent_quality_questions.sql` |
| `JN0-663` | JNCIP-SP | `generators.jncip:generate_jncip_sp` | `080_jncip_sp_quality_questions.sql` |

### Generate all migrations

```bash
python3 scripts/generate_quality_questions.py
```

Generate a single exam:

```bash
python3 scripts/generate_quality_questions.py ccna
python3 scripts/generate_quality_questions.py jncia-junos
python3 scripts/generate_quality_questions.py jncip-ent
python3 scripts/generate_quality_questions.py jncip-sp
```

### Validate output

Run the in-memory validator for structural correctness:

```bash
python3 - <<'PY'
import sys
sys.path.insert(0, 'scripts')
from generators.ccna import generate_ccna
# Replace with the generator under test
qs = generate_ccna(total=1000, seed=42)
print('Total:', len(qs))
PY
```

### Apply migrations locally

Start PostgreSQL (Docker example):

```bash
docker run -d --name netcert-test-pg \
  -e POSTGRES_USER=netcert \
  -e POSTGRES_PASSWORD=netcert \
  -e POSTGRES_DB=netcert \
  -p 5432:5432 postgres:16
```

Apply migrations:

```bash
cd backend
go run github.com/pressly/goose/v3/cmd/goose@latest \
  -dir migrations postgres \
  'postgresql://netcert:netcert@localhost:5432/netcert' up
```

### Adding new content

1. Add items to the relevant pool file (`scripts/generators/ccna_pools.py`, `junos_pools.py`, `jncip_pools.py`).
2. Adjust generator counts in the corresponding `scripts/generators/*.py` file if needed.
3. Regenerate the migration and test it with `goose`.

### Coding style

- Use `random.Random(seed)` for reproducible output.
- All question builders (`make_single_choice`, `make_multiple_choice`, etc.) live in `scripts/generators/common.py`.
- Use dollar-quoting (`$$...$$`) for PostgreSQL string literals; wrap each statement with `-- +goose StatementBegin` / `-- +goose StatementEnd`.
- Keep question bodies unique per exam (`unique_questions`).
- Prefer real CLI output and scenarios for `simlet` items.
