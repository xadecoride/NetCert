[English](README.md) | [Русский](README.ru.md)

# NetCert

Local Cisco and Juniper certification practice with a Go API, a Next.js interface and PostgreSQL question banks. The core workflow is registration, exam selection, answering questions, reviewing explanations and keeping attempt history.

NetCert is an independent practice project, not an official Cisco or Juniper product. Catalog labels and generated questions do not establish alignment with the latest official exam blueprints, complete certification coverage or exam readiness.

## Implemented scope

| Area | What is present in the source |
|---|---|
| Accounts | Registration, login, bcrypt password hashing, JWT access tokens and profile/preferences endpoints |
| Practice exams | Track/exam catalog, question retrieval, attempt creation, answer submission, completion and history |
| Question interaction | Single choice, multiple choice and fill-in-the-blank; text-based simlets use single-choice grading |
| Study | Study pages, guide completion tracking and quick-lab content endpoints |
| Content | PostgreSQL migrations and Python question-bank generators |
| Experimental labs | Lab/session endpoints, WebSocket terminals, Containerlab topology files and Python grading scripts; require separate infrastructure |

Declared question types such as drag-and-drop or topology do not mean that a complete interactive renderer and grader exist for them. Live labs are not included in the default Compose startup.

## Architecture

```text
Browser / Next.js UI
  -> Go HTTP API (Chi + JWT middleware)
  -> use cases
  -> PostgreSQL repositories (pgx)
  -> accounts, questions, answers, attempts and study progress

Python content generators -> goose SQL migrations -> PostgreSQL question banks

Separate experimental path:
Go lab endpoints / WebSockets -> Containerlab / Docker -> lab nodes and graders
```

| Layer | Stack |
|---|---|
| Backend | Go 1.25.7, Chi v5, pgx/v5, goose v3, JWT, bcrypt, Gorilla WebSocket |
| Frontend | Next.js 15, React 19, TypeScript, Tailwind CSS 4; xterm and React Flow components for lab views |
| Database | PostgreSQL 16 |
| Content tooling | Python scripts producing SQL migrations |
| Development infrastructure | Docker Compose; Redis 7 is declared, but runtime Redis use was not found in the inspected backend paths |
| Experimental lab infrastructure | Containerlab, Docker-in-Docker, Juniper cRPD, Alpine sandbox, FRRouting and Python graders |

## Quick start: local practice

Requirements: Git, Docker Engine and Docker Compose v2.

```bash
git clone https://github.com/xadecoride/NetCert.git
cd NetCert
cp .env.example .env
# Review .env: database credentials, JWT_SECRET and host ports.
docker compose up --build -d
docker compose ps
```

Default addresses:

| Service | Address |
|---|---|
| UI | http://localhost:3000 |
| API health | http://localhost:8080/health |

The Compose file defines PostgreSQL, Redis, a one-shot migration service, the backend and the frontend. Backend startup also runs embedded goose migrations. The defaults are for local development: replace credentials and JWT secrets before exposing any service outside a trusted lab, and restrict published database/Redis ports.

```bash
docker compose logs -f migrations backend frontend
docker compose down
```

`docker compose down` stops the stack without removing named data volumes. Do not remove volumes if you need to preserve users and attempt history.

These commands are derived from the checked-in configuration; a full container build and startup were not performed for this documentation update.

### Native development

Use Go **1.25.7 or newer**, Node.js 22+, npm and a local PostgreSQL 16 instance. Copy `backend/.env.example` to `backend/.env` and configure its database DSN and JWT secret locally. The application database must exist before backend startup.

In separate terminals, from the repository root:

```bash
cd backend
go run ./cmd/server/
```

```bash
cd frontend
npm ci
npm run dev
```

Python is needed for content generation, not for the Go API itself. Redis is part of the provided Compose configuration, but an active cache or queue integration is not established by its presence there.

## Using the application

1. Open the UI and register at `/auth/register`, or sign in at `/auth/login`.
2. Select a track/exam in `/exams` and start an attempt.
3. Submit answers and complete the attempt to calculate its result.
4. Review the result, explanations and attempt history; use study pages for guide progress.
5. Treat interactive labs as a separate environment: a terminal UI alone does not mean that a sandbox or network node is available.

The API uses `/api/v1`; authenticated HTTP requests use an access token in `Authorization: Bearer …`. The route definitions are in [router.go](backend/internal/delivery/http/router.go).

| Route group | Examples |
|---|---|
| Authentication | `POST /api/v1/auth/register`, `POST /api/v1/auth/login` |
| Catalog | `GET /api/v1/tracks`, `GET /api/v1/tracks/{slug}/exams` |
| Attempts | `POST /api/v1/attempts`, `POST /api/v1/attempts/{attemptId}/answers`, `POST /api/v1/attempts/{attemptId}/complete` |
| History | `GET /api/v1/attempts/history` |
| Study | `GET /api/v1/study/progress`, `POST /api/v1/study/progress/toggle` |
| Labs | `/api/v1/labs`, `/api/v1/quick-labs` and authenticated `/ws/...` endpoints |

## Question-bank generation

The current generator entry point has four targets:

| Target | Output in `backend/migrations/` |
|---|---|
| `ccna` | `077_ccna_quality_questions.sql` |
| `jncia-junos` | `078_jncia_junos_quality_questions.sql` |
| `jncip-ent` | `079_jncip_ent_quality_questions.sql` |
| `jncip-sp` | `080_jncip_sp_quality_questions.sql` |

```bash
# Generate one target; omit the argument to generate all four.
python3 scripts/generate_quality_questions.py ccna
git diff -- backend/migrations
```

**Run this only in a disposable development copy/database until you have reviewed the output.** The generator overwrites migration files `077`–`080`, and the generated SQL deletes existing questions for the corresponding exams before inserting replacements. Editing an already-applied goose migration does not automatically reapply it to an existing database. Generation is content maintenance, not a safe live update command.

## Experimental lab path

[infra/docker-compose.staging.yml](infra/docker-compose.staging.yml) defines a separate staging stack with a privileged DinD service, an Alpine sandbox and FRRouting. Lab definitions and graders are under [backend/labs](backend/labs); orchestration and WebSocket handling live in the Go backend.

Do not treat this as a working one-command lab deployment:

- The backend Dockerfile does not install the `containerlab` binary, although orchestration expects it.
- The staging backend runs as a non-root user while mounting the host Docker socket; access and isolation need explicit validation.
- Vendor images, device access, terminal routing and grading require environment-specific setup.
- The staging migration service executes SQL through `psql`; it is not the same migration workflow as the default Compose service.

Use an isolated lab host. Do not expose Docker/DinD APIs, raw terminals or development credentials publicly.

## Repository map

```text
backend/cmd/server/              API entry point and dependency wiring
backend/internal/delivery/       HTTP and WebSocket handlers
backend/internal/usecase/        Authentication, exams, study and lab workflows
backend/internal/repository/     PostgreSQL access
backend/migrations/              Schema and question-bank migrations
backend/labs/                    Experimental topologies and graders
frontend/                        Next.js pages, components and API client
scripts/                         Content generators and maintenance utilities
infra/                           Dockerfiles and staging/lab configuration
```

## Verification and limitations

Local check on **18 November 2026**, against source revision `f686d5c` before this documentation change:

```bash
cd backend
go test ./internal/...
```

The command **fails**: `internal/usecase/auth_usecase_test.go:83` references `AuthResponse.RefreshToken`, which is absent from the current model. HTTP-handler and PostgreSQL-repository test packages passed in that run. This is not a passing backend suite, a live-lab test or a full-stack acceptance result.

Additional boundaries found during source inspection:

- Authentication uses access tokens; refresh-token behavior must not be inferred from the stale test.
- Lab pause/resume updates submission status in the database; it does not implement device snapshots or suspension.
- The WebSocket SSH proxy passes submission/user identifiers in an order that differs from the use-case signature; ownership/session behavior needs correction and tests.
- Some exam formats have model declarations or static content without complete UI/grading support.
- Question correctness and current official blueprint alignment require independent review.
- Development secrets, published service ports and privileged lab services need hardening before any shared deployment.

## Roadmap

- Align authentication tests with the implemented token model.
- Verify migrations and repeatable startup against a clean database.
- Review question-bank content and document coverage by actual question format and exam target.
- Complete missing interactive renderers/graders or explicitly narrow the supported types.
- Validate lab ownership checks, Containerlab installation, terminal access and grading end to end.
- Implement and test real lab lifecycle behavior before claiming snapshot-based pause/resume.

## License

[AGPL-3.0](LICENSE). Not affiliated with Cisco Systems or Juniper Networks.
