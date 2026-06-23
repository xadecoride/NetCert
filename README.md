# NetCert

A free, open-source platform for preparing for **Juniper (JNCIA → JNCIE)** and **Cisco (CCNA → CCIE)** certification exams. Register, pick a track, and start practicing.

---

## Quick Start

Clone the repo and start the whole stack in a few commands.

### 1. Clone the repository

```bash
git clone <repo-url>
cd NetCert
```

### 2. Start everything with Docker Compose (recommended)

```bash
cp backend/.env.example backend/.env
make up
```

This builds and starts PostgreSQL, Redis, backend, and frontend in one command. Migrations are applied automatically before the backend starts.

Stop the stack:

```bash
make down
```

### Alternative: run services separately

Start infrastructure:

```bash
make dev-infra
```

Then in two separate terminals:

```bash
make dev-backend   # http://localhost:8080
```

```bash
make dev-frontend  # http://localhost:3000
```

---

## Prerequisites

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose plugin
- [Go 1.22+](https://go.dev/doc/install)
- [Node.js 22+](https://nodejs.org/)
- `make`

---

## URLs

| URL | Description |
|-----|-------------|
| `http://localhost:3000` | Landing page |
| `http://localhost:3000/auth/register` | Sign up |
| `http://localhost:3000/auth/login` | Sign in |
| `http://localhost:3000/dashboard` | Dashboard |
| `http://localhost:3000/exams` | Exam catalog |
| `http://localhost:8080/health` | API health check |

---

## Useful Commands

```bash
make dev-infra      # Start Postgres and Redis
make migrate-up     # Apply migrations
make dev-backend    # Run Go server on :8080
make dev-frontend   # Run Next.js dev server on :3000
```

---

## Generating Question Banks

Question banks are produced from blueprint-aligned content pools and written as `goose` migrations in `backend/migrations/`.

Generate all supported exams:

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

Then apply migrations:

```bash
cd backend
make migrate-up
```

See `AGENTS.md` for detailed instructions on adding new content and validating output.

---

## Project Structure

```
NetCert/
├── backend/                    # Go backend (Clean Architecture)
│   ├── cmd/server/main.go      # Entry point
│   ├── internal/
│   │   ├── config/             # Configuration
│   │   ├── domain/             # Domain models
│   │   ├── repository/postgres/# Repositories
│   │   ├── usecase/            # Business logic
│   │   ├── delivery/http/      # HTTP handlers (Chi)
│   │   ├── middleware/         # JWT auth middleware
│   │   └── pkg/                # Utilities
│   └── migrations/             # SQL migrations and seed data
├── frontend/                   # Next.js frontend
│   ├── app/                    # App Router pages
│   ├── components/             # UI components
│   └── lib/                    # API client, context, utilities
└── infra/                      # Docker infrastructure
    └── docker-compose.yml
```

---

## Tech Stack

**Backend**

- Go 1.22+
- Chi router
- pgx PostgreSQL driver
- JWT authentication (access + refresh tokens)
- Clean Architecture

**Frontend**

- Next.js 16 with App Router
- React 19 + TypeScript
- Tailwind CSS 4
- shadcn/ui
- Framer Motion
- Recharts

**Infrastructure**

- PostgreSQL 16
- Redis 7
- Docker Compose

---

## API Overview

| Method | Path | Description |
|--------|------|-------------|
| GET | `/health` | Health check |
| POST | `/api/v1/auth/register` | Register |
| POST | `/api/v1/auth/login` | Log in |
| GET | `/api/v1/users/me` | Current user profile |
| GET | `/api/v1/tracks` | List certification tracks |
| GET | `/api/v1/tracks/{slug}` | Track details |
| GET | `/api/v1/tracks/{slug}/exams` | Exams in a track |
| GET | `/api/v1/exams/{examId}` | Exam details |
| POST | `/api/v1/attempts` | Start an attempt |
| GET | `/api/v1/attempts/{attemptId}` | Get attempt |
| POST | `/api/v1/attempts/{attemptId}/answers` | Submit answer |
| POST | `/api/v1/attempts/{attemptId}/complete` | Complete attempt |
| GET | `/api/v1/attempts/history` | Attempt history |

---

## Sample Content

Seed data includes starter questions for:

- **JNCIA-Junos (JN0-101)** — Junos OS, CLI, OSPF, BGP, firewall filters, static routing, interfaces
- **JNCIA-SP (JN0-201)** — MPLS fundamentals, architecture, LDP
- **CCNA (200-301)** — OSPF AD, VLAN ranges, RIP

---

## Roadmap

- [ ] 16 full exams across JNCIA–JNCIE and CCNA–CCIE
- [ ] JNCIE Lab Engine (Containerlab)
- [ ] Spaced repetition (SM-2)
- [ ] Analytics: heatmap, radar chart, readiness score
- [ ] Gamification: streaks, XP, achievements
- [ ] i18n (EN/RU)
- [ ] OAuth2 (Google/GitHub)
- [ ] PWA / offline mode
