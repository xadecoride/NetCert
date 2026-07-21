# Contributing to NetCert

Thank you for your interest in contributing! NetCert is a free, open-source
platform for network certification exam preparation, licensed under AGPL-3.0.

## Quick Start

1. Fork the repository
2. Clone your fork: `git clone https://github.com/<you>/NetCert.git`
3. Create a branch: `git checkout -b feat/your-feature`
4. Make changes, commit with [Conventional Commits](https://www.conventionalcommits.org/)
5. Push and open a Pull Request

## Development Setup

```bash
# Prerequisites: Docker, Go 1.22+, Node 22+, Make
cp backend/.env.example backend/.env
make up          # starts Postgres, Redis, Backend, Frontend (with auto-migrations)
```

Backend API: http://localhost:8080
Frontend: http://localhost:3000

## Code Style

### Backend (Go)
- **Clean Architecture** layers: `domain/` → `repository/postgres/` → `usecase/` → `delivery/`
- Run `golangci-lint run` before pushing
- Struct tags: `json:"snake_case"` for API, `db:"snake_case"` for DB
- Errors: use domain sentinel errors (`domain.ErrNotFound`, `domain.ErrForbidden`, etc.)
- Tests: `go test ./...` — aim for coverage on new code

### Frontend (Next.js / React / TypeScript)
- Strict TypeScript (`strict: true`)
- Components in `components/`, pages in `app/`
- Run `npm run lint` before pushing
- Use `@/` path aliases
- i18n: add keys to both `lib/i18n/locales/en.ts` and `ru.ts`

### Content (Questions / Labs)
- Questions must be **100% original** — no braindump/NDA content
- Follow the JSON schema in `AGENTS.md`
- Run `scripts/audit/audit_questions.py` after adding questions
- Lab configs: `backend/labs/micro-labs/` — follow existing structure

## Commit Messages

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
feat(labs): add OSPF adjacency micro-lab
fix(auth): validate email format on registration
docs(readme): add Cisco CCNP section
refactor(usecase): extract domain errors into errors.go
```

## Pull Request Checklist

- [ ] `go build ./...` passes
- [ ] `go vet ./...` passes
- [ ] `npm run build` passes
- [ ] New backend code has tests
- [ ] No secrets/credentials committed
- [ ] Commit messages follow Conventional Commits
- [ ] Documentation updated if needed

## Reporting Issues

When filing bugs, please include:
- OS and versions (Go, Node, Docker)
- Steps to reproduce
- Expected vs actual behavior
- Relevant logs (backend logs, browser console)

## Questions?

Open an issue with the `question` label, or join our Telegram community (see README).
