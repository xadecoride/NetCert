# NetCert

A free, open-source platform for preparing for **Juniper (JNCIA → JNCIE)** and **Cisco (CCNA → CCIE)** certification exams. Register, pick a track, and start practicing.

---

## Quick Start (Native — No Docker Required)

### Prerequisites

| Tool | Version | Install (Fedora/RHEL) | Install (Ubuntu/Debian) |
|------|---------|----------------------|------------------------|
| **Go** | 1.22+ | `dnf install golang` | `apt install golang` |
| **Node.js** | 22+ | `dnf install nodejs` | `apt install nodejs` |
| **PostgreSQL** | 16+ | `dnf install postgresql-server postgresql-contrib` | `apt install postgresql postgresql-contrib` |
| **Redis** | 7+ | `dnf install redis` | `apt install redis` |

> **This project runs natively without Docker.** Docker is only needed for Containerlab (JNCIE/CCIE labs) — not for the main app.

---

### 1. Clone & Configure

```bash
git clone <repo-url>
cd NetCert

# Backend config
cd backend
cp .env.example .env
# .env already has correct values for local Postgres/Redis (127.0.0.1:5432, 127.0.0.1:6379)
```

### 2. Setup Database (one-time)

```bash
# Fedora/RHEL:
sudo postgresql-setup --initdb
sudo systemctl enable --now postgresql redis

# Ubuntu/Debian:
# sudo systemctl enable --now postgresql redis

# Create DB user & database
sudo -u postgres psql -c "CREATE USER netcert WITH PASSWORD 'netcert';"
sudo -u postgres psql -c "CREATE DATABASE netcert OWNER netcert;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE netcert TO netcert;"
sudo -u postgres psql -d netcert -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"
```

### 3. Run Migrations

```bash
cd /home/lecoo/NetCert/backend
go install github.com/pressly/goose/v3/cmd/goose@latest
export PATH=$PATH:$(go env GOPATH)/bin

# IMPORTANT: Use 127.0.0.1 (not localhost) to force TCP/IP with md5 auth
goose -dir migrations postgres "postgresql://netcert:netcert@127.0.0.1:5432/netcert?sslmode=disable" up
```

### 4. Start Services (two terminals)

**Terminal 1 — Backend:**
```bash
cd /home/lecoo/NetCert/backend
go run ./cmd/server/
# API: http://localhost:8080
```

**Terminal 2 — Frontend:**
```bash
cd /home/lecoo/NetCert/frontend
npm ci
npm run dev
# UI: http://localhost:3000 (or 3001 if 3000 busy)
```

---

## Access Points

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
# Backend
cd backend && go run ./cmd/server/

# Frontend
cd frontend && npm run dev

# Migrations
cd backend
export PATH=$PATH:$(go env GOPATH)/bin
goose -dir migrations postgres "postgresql://netcert:netcert@127.0.0.1:5432/netcert?sslmode=disable" up

# Database management
sudo systemctl restart postgresql redis
sudo systemctl status postgresql redis

# Frontend deps
cd frontend && npm ci
```

---

## Generating Question Banks

Question banks are produced from blueprint-aligned content pools and written as `goose` SQL migrations in `backend/migrations/`.

```bash
# All exams
python3 scripts/generate_quality_questions.py

# Single exam
python3 scripts/generate_quality_questions.py ccna
python3 scripts/generate_quality_questions.py jncia-junos
python3 scripts/generate_quality_questions.py jncip-ent
python3 scripts/generate_quality_questions.py jncip-sp
```

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
├── scripts/                    # Question generators, audits
├── infra/                      # Docker infrastructure (for Containerlab only)
│   └── docker-compose.yml
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
- Containerlab v0.75 (for JNCIE/CCIE labs — requires Docker)

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

## Troubleshooting

### Database connection failed
- Check `backend/.env` has `DATABASE_DSN=postgres://netcert:***@127.0.0.1:5432/netcert?sslmode=disable`
- **Use `127.0.0.1` not `localhost`** — forces TCP/IP with md5 auth
- Ensure Postgres is running: `systemctl status postgresql`
- Ensure `uuid-ossp` extension exists: `sudo -u postgres psql -d netcert -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"`

### Port already in use (3000 or 8080)
```bash
lsof -ti:3000 | xargs kill -9
lsof -ti:8080 | xargs kill -9
```

### Frontend build fails
```bash
cd frontend
rm -rf node_modules .next package-lock.json
npm ci
npm run build
```

### PostgreSQL: `Ident authentication failed`
- You used `localhost` in DSN — change to `127.0.0.1`
- Or edit `/var/lib/pgsql/data/pg_hba.conf`: change `local all all peer` → `local all all trust`, then `systemctl restart postgresql`

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