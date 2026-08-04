# NetCert

A free, open-source platform for preparing for **Juniper (JNCIA → JNCIE)** and **Cisco (CCNA → CCIE)** certification exams. Register, pick a track, and start practicing.

---

## Quick Start

### Prerequisites

| Tool | Version | Install |
|------|---------|---------|
| **Docker** | 24+ | [docker.com](https://docs.docker.com/get-docker/) |
| **Docker Compose** | v2 (plugin) | Included with Docker Desktop / `apt install docker-compose-plugin` |
| **Go** | 1.22+ | [go.dev](https://go.dev/doc/install) |
| **Node.js** | 22+ | [nodejs.org](https://nodejs.org/) |
| **Make** | any | `apt install make` / `brew install make` |

> **No Docker?** See [Alternative: Run services separately](#alternative-run-services-separately) below.

---

### 1. Clone the repository

```bash
git clone <repo-url>
cd NetCert
```

---

### 2. Start everything with Docker Compose (recommended)

```bash
# Configure environment
cp backend/.env.example backend/.env

# Build and start Postgres, Redis, Backend, Frontend
make up
```

This builds and starts all services in one command. Migrations are applied automatically before the backend starts.

**Access points:**
| URL | Description |
|-----|-------------|
| `http://localhost:3000` | Landing page |
| `http://localhost:3000/auth/register` | Sign up |
| `http://localhost:3000/auth/login` | Sign in |
| `http://localhost:3000/dashboard` | Dashboard |
| `http://localhost:3000/exams` | Exam catalog |
| `http://localhost:8080/health` | API health check |

**Stop the stack:**
```bash
make down
```

---

### Alternative: Run services separately (no Docker Compose)

If you have Postgres/Redis running locally or on a remote host:

```bash
# 1. Start only infrastructure (Postgres + Redis) — requires Docker
make dev-infra

# 2. In separate terminals:
make dev-backend   # http://localhost:8080
make dev-frontend  # http://localhost:3000
```

#### Fully local (no Docker at all)

You need a running **PostgreSQL 16** and **Redis 7** instance.

```bash
# 1. Configure database connection
cp backend/.env.example backend/.env
# Edit backend/.env with your POSTGRES_DSN and REDIS_ADDR

# 2. Apply migrations
cd backend
go run github.com/pressly/goose/v3/cmd/goose@latest \
  -dir migrations postgres \
  "$POSTGRES_DSN" up

# 3. Run backend
go run ./cmd/server

# 4. In another terminal, run frontend
cd ../frontend
npm ci
npm run dev
```

---

## Useful Commands

```bash
make dev-infra      # Start Postgres and Redis only
make migrate-up     # Apply database migrations
make dev-backend    # Run Go server on :8080
make dev-frontend   # Run Next.js dev server on :3000
make down           # Stop all Docker containers
make clean          # Stop containers + remove volumes (data loss!)
```

---

## Generating Question Banks

Question banks are produced from blueprint-aligned content pools and written as `goose` SQL migrations in `backend/migrations/`.

### Generate all supported exams

```bash
python3 scripts/generate_quality_questions.py
```

### Generate a single exam

```bash
python3 scripts/generate_quality_questions.py ccna
python3 scripts/generate_quality_questions.py jncia-junos
python3 scripts/generate_quality_questions.py jncip-ent
python3 scripts/generate_quality_questions.py jncip-sp
```

### Apply migrations locally

```bash
# Start PostgreSQL (Docker example)
docker run -d --name netcert-test-pg \
  -e POSTGRES_USER=netcert \
  -e POSTGRES_PASSWORD=netcert \
  -e POSTGRES_DB=netcert \
  -p 5432:5432 postgres:16

# Apply migrations
cd backend
go run github.com/pressly/goose/v3/cmd/goose@latest \
  -dir migrations postgres \
  'postgresql://netcert:netcert@localhost:5432/netcert' up
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
├── infra/                      # Docker infrastructure
│   └── docker-compose.yml
├── scripts/                    # Question generators, audits
└── CLAUDE.md                   # Project source of truth for AI agents
```

---

## Tech Stack

**Backend**
- Go 1.25.7
- Chi router (v5)
- pgx/v5 PostgreSQL driver
- JWT authentication (HS256, access tokens only)
- Clean Architecture
- goose v3 (SQL migrations, embedded)
- gorilla/websocket (lab terminals)

**Frontend**
- Next.js 15.2 (App Router)
- React 19 + TypeScript 5.7 (strict)
- Tailwind CSS 4 (`@theme`)
- Manual shadcn-style components (CVA + clsx + tailwind-merge)
- Framer Motion 11
- Recharts 2.15
- @xterm/xterm 6 (terminals)
- @xyflow/react 12 (topology)

**Infrastructure**
- PostgreSQL 16
- Redis 7
- Docker Compose
- Containerlab v0.75 (for JNCIE/CCIE labs)

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
| GET | `/api/v1/labs` | List labs |
| POST | `/api/v1/labs/start` | Start lab session |
| GET | `/api/v1/labs/submissions/{id}` | Get lab submission |
| WS | `/ws/...` | Lab terminals (JWT via `?token=`) |

---

## Sample Content

Seed data includes starter questions for:
- **JNCIA-Junos (JN0-106)** — Junos OS, CLI, OSPF, BGP, firewall filters, static routing, interfaces
- **JNCIP-ENT (JN0-649)** — BGP, EVPN, IS-IS, MPLS, multicast
- **JNCIP-SP (JN0-663)** — MPLS, BGP-LU, LDP, RSVP, Inter-AS
- **CCNA (200-301)** — OSPF AD, VLAN ranges, RIP, wireless basics

---

## Troubleshooting

### `make: docker: No such file or directory`
Docker is not installed. Install it:
- **Ubuntu/Debian:** `sudo apt update && sudo apt install docker.io docker-compose-plugin`
- **Fedora:** `sudo dnf install docker docker-compose`
- **Arch:** `sudo pacman -S docker docker-compose`
- **macOS:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Windows:** Install [Docker Desktop](https://www.docker.com/products/docker-desktop/) with WSL2 backend

Then run `make up` again.

### Port already in use (3000 or 8080)
```bash
# Find and kill the process
lsof -ti:3000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
```

### Database connection failed
- Check `backend/.env` has correct `POSTGRES_DSN`
- Ensure Postgres is running: `docker ps | grep postgres`
- Run migrations manually: `make migrate-up`

### Frontend build fails
```bash
cd frontend
rm -rf node_modules .next package-lock.json
npm ci
npm run build
```

---

## License

AGPL-3.0 — see [LICENSE](LICENSE).

> **Disclaimer:** NetCert — Certification Preparation Platform. Not affiliated with Juniper Networks or Cisco Systems.

---

## Roadmap

- [ ] 16 full exams across JNCIA–JNCIE and CCNA–CCIE
- [ ] JNCIE Lab Engine (Containerlab)
- [ ] Spaced repetition (SM-2 / FSRS)
- [ ] Analytics: heatmap, radar chart, readiness score
- [ ] Gamification: streaks, XP, achievements
- [ ] i18n (EN/RU — partially done)
- [ ] OAuth2 (Google/GitHub)
- [ ] PWA / offline mode