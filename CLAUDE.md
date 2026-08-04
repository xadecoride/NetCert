# NetCert — Project Source of Truth

> **Этот файл — единый источник правды для нейросетей-агентов.**
> Все остальные `.md` аудиты (AUDIT_TECHNICAL, AUDIT_BUSINESS, ROADMAP_DEV, IDEAS_INITIATIVES) — исторические артефакты-спецификации. Расхождения трактуются в пользу CLAUDE.md (если в аудите сказано «не реализовано», но в CLAUDE.md отмечено «✅ сделано» — CLAUDE.md прав).
> Архитектурные решения — в CONTRIBUTING.md / LAB_METHODOLOGY.md (ссылки ниже).

**Дата последнего обновления:** 2026-08-04

---

## 1. Что такое NetCert

**NetCert** — бесплатная open-source (AGPL-3.0) платформа подготовки сетевых инженеров к сертификационным экзаменам **Juniper (JNCIA → JNCIE)** и **Cisco (CCNA → CCIE)**. Это НЕ PKI/TLS-сертификаты — это профессиональная сетевая сертификация вендоров.

Ключевые фичи (реализованы в коде):
- Банк вопросов (~9 150 активных после чистки миграцией 063)
- Тайм-симуляция экзаменов (attempts + история)
- Типы вопросов: single/multiple choice, fill-blank, simlet (CLI-сценарии), топология/диаграммы
- «Deep Dive» объяснения с версионированием (TL;DR / scenario / why_correct / distractor_analysis / cli_examples / vendor_nuances)
- Live CLI-песочницы через WebSocket: Alpine, FRRouting (VTYSH), cRPD (Junos CLI)
- Лабораторные: микро-лабы (теория), Containerlab (cRPD/FRR), full exam labs
- Quick Labs — облегчённые направляемые лабы
- Интерактивный просмотр топологии на React Flow (@xyflow/react)
- Дашборд с аналитикой готовности (recharts)
- Геймификация: streaks, XP, достижения (частично)
- i18n EN/RU

Дисклеймер в футере: «NetCert — Certification Preparation Platform. Not affiliated with Juniper Networks or Cisco Systems.» (см. `frontend/lib/i18n/locales/{en,ru}.ts:54`).

---

## 2. Бизнес-модель

**Free / Open Source навсегда. Без платных тиров.** Решение владельца. В коде нет ни одной платёжной интеграции.

Лендинговый copy НЕ должен содержать:
- «1,200+ Active learners» — недоказуемо (нет аналитики). Заменять на «Self-hostable / Open Source».
- «AI-adaptive / FSRS» — не реализовано (attempts используют `math/rand`). Убрать или реализовать (Фаза 3.1).
- Противоречивые числа вопросов («9,150+» vs «1,200+ original») — сводить к одному источнику (live-запрос к БД / константа).

**Ключевые бизнес-риски (из аудитов):**
1. Нет LICENSE — блокирует OSS-нарратив (добавлен AGPL-3.0)
2. Маркетинг-заявления (FSRS, «1 200+ learners») не подтверждены кодом
3. Bus factor = 1 — без комьюнити проект уязвим
4. Тяжёлые лабы (JNCIE/CCIE 8-часовые) требуют десятки GB RAM/сессию — в free-модели стратегия: self-host-first + WASM/micro-labs + ограниченный демо-concurrency

**Пути устойчивости без монетизации:**
- GitHub Sponsors / Open Collective / Boosty
- Гранты (NGI / Sovereign Tech Fund / NLnet)
- B2B-деплой (интеграция/поддержка/кастомизация)
- Партнёрство с учебными центрами (Juniper ATP, Cisco Learning Partners)
- Контент-контрибуции сообщества

---

## 3. Текущая фаза разработки

| Фаза | Статус | Замечание |
|------|--------|-----------|
| **0. Hotfix безопасности (P0)** | ✅ закрыта | IDOR-stop, WS auth, validator, refresh-token removal |
| 0.3 — ownership-проверка в `ws/ssh_proxy.go handleTerminal` | ⏳ TODO | auth есть, ownership нет |
| **1. Фундамент качества (P1)** | частично | CI, линтеры, гигиена ✅ ; тесты lab_usecase, единый error-маппер, контент-вне-git — TODO |
| **2. Frontend cleanup (P1)** | 🔴 НЕ НАЧАТА | целевая зона для frontend-работы (см. §7) |
| 3. Продуктовый parity (P2) | backlog | FSRS, честный copy, recharts-визуализации |
| 4. OSS-зрелость (P2) | частично | LICENSE/CONTRIBUTING/CODE_OF_CONDUCT/PR-templates ✅; README-бейджи, Telegram, prod-deploy — TODO |

---

## 4. Технологический стек

**Бэкенд:**
- Go **1.25.7** (не 1.22 — старый README был drift, обновлён)
- Chi v5.1.0, pgx/v5.9.2 (pgxpool), pgxmock для тестов
- golang-jwt/v5, HS256, access-only (refresh удалён в Фазе 0.4)
- bcrypt (DefaultCost), validator/v10 v10.26.0 (подключён в Фазе 0.4)
- goose v3.20.0 (SQL-миграции через `embed.FS`, авто-апплай на старте)
- gorilla/websocket v1.5.3 (терминалы лаб + stream топологии)
- golang.org/x/crypto/ssh (`InsecureIgnoreHostKey()` — acceptable для эфемерных лаб, задокументировано)
- testify v1.11.1
- log/slog (JSON в stdout)

**Фронтенд:**
- **Next.js ^15.2.4** (не 16 — зафиксировано как целевое)
- React 19, TypeScript 5.7 strict, `@/*` aliases
- Tailwind CSS v4 (`@theme`), manual shadcn (CVA + clsx + tailwind-merge — НЕ через CLI)
- lucide-react, @phosphor-icons/react, @radix-ui/react-icons
- framer-motion v11 (motion-обёртки в `frontend/components/motion/*`)
- recharts v2.15 (используется только в dashboard)
- @xterm/xterm v6 + addon-fit + addon-webgl (терминалы лаб)
- @xyflow/react v12 (просмотр топологии)
- next-themes, sonner (toast), zod v3.24 (почти не используется)
- **НЕ установлены:** TanStack Query (TODO §7.2), Vitest/Jest/Playwright (TODO §7.7), next-pwa (TODO §7.4)

**Инфра:**
- PostgreSQL 16, Redis 7
- Containerlab v0.75.0 + DinD (cRPD/FRR топологии; cRPD требует Juniper license)
- Non-root users
- CI: `.github/workflows/ci.yml` — matrix backend (go build/vet/test) + frontend (npm ci/lint/build)

---

## 5. Архитектура

### 5.1 Бэкенд — Clean Architecture

```
domain/            ← чистые сущности + интерфейсы репозиториев + sentinel-ошибки
  └ repository/postgres/   ← реализация репозиториев (pgx)
      └ usecase/           ← бизнес-логика (DI через интерфейсы)
          └ delivery/
              ├ http/       ← Chi handlers
              └ ws/         ← WebSocket (SSH proxy, sandbox)
```

Sentinel-ошибки (`backend/internal/domain/errors.go`):
- `ErrNotFound` → 404
- `ErrForbidden` → 403 (IDOR-защита: `sub.UserID != userID`)
- `ErrConflict` → 409
- `ErrValidation` → 400 (после `validator.Struct()`)

Паттерны:
- JWT fail-fast guard в `config.go:49-60` (сервер отказывается стартовать с небезопасными секретами в не-dev).
- JWT подпись явно pinned к HMAC — блокирует `alg:none`-атаку (`jwt.go:66-68`).
- Анти-enumeration на login: одинаковый `ErrInvalidCredentials` для «user not found» и «wrong password».
- WS endpoints (`/ws/*`) — под `authMw.AuthenticateWS` (Bearer header или `?token=` query param). **TODO §3: проверка владельца сабмишена в ssh_proxy.handleTerminal.**
- Структурированный лог: `slog` JSON в stdout.

### 5.2 Фронтенд — Next.js App Router

- `frontend/app/**` — App Router pages
- `frontend/components/` — UI (ui/*, layout/*, motion/*, lab/*)
- `frontend/lib/` — `api.ts` (fetch-обёртка), `auth-context.tsx`, `i18n/`, `with-auth.tsx`, `topology/`, `utils.ts`, `motion.ts`
- Проксирование `/api/* → backend:8080/api/v1/*` через `next.config.ts rewrites` (исключает CORS)
- `/ws/* → backend/ws/*` также через rewrite
- Auth: `access_token` в `localStorage`, ручной `fetch`+`useState/useEffect` через `lib/api.ts`
  - **TODO §7.2:** мигрировать на TanStack Query (`useQuery`/`useMutation`)
- `AuthContext` оборачивает профиль; `withAuth` HOC редиректит неавторизованных → `/auth/login`
- i18n: кастомный context (`lib/i18n/context.tsx`), локализированы `/study` и `/dashboard`. **Правило:** при добавлении i18n-ключа — добавить в оба `en.ts` и `ru.ts`.
- **Все 10 страниц сейчас `'use client'`** — 0 Server Components. **TODO §7.5:** перевести read-only (landing, `/exams` catalog, `/study`) на RSC.

---

## 6. API-контракт (актуальный — `backend/internal/delivery/http/router.go`)

### Public
- `GET /health` → `{"status":"ok","version":"1.0.0"}`
- `POST /api/v1/auth/register` — body `{email, password, display_name}` → `{user, access_token, expires_in}`
- `POST /api/v1/auth/login` — body `{email, password}` → `{user, access_token, expires_in}`
- `GET /api/v1/tracks` — список треков
- `GET /api/v1/tracks/{slug}` — детали трека
- `GET /api/v1/tracks/{slug}/exams` — экзамены трека
- `GET /api/v1/sandbox/status` — health sandbox

### Protected (JWT Bearer)
- `GET /api/v1/users/me` — профиль
- `PATCH /api/v1/users/me` — `{display_name?, avatar_url?}`
- `PUT /api/v1/users/me/preferences` — `{language?, theme?, notifications?}`
- `PUT /api/v1/users/me/email` — `{email}`
- `GET /api/v1/exams/{examId}` — детали экзамена
- `GET /api/v1/exams/{examId}/questions?lang=` — вопросы экзамена
- `POST /api/v1/attempts` — `{exam_id, mode: exam|practice|timed, question_count?}` → Attempt
- `GET /api/v1/attempts/{attemptId}` — состояние попытки
- `GET /api/v1/attempts/{attemptId}/questions` — вопросы попытки
- `GET /api/v1/attempts/{attemptId}/details` — AttemptWithDetails (для review)
- `POST /api/v1/attempts/{attemptId}/answers` — `{question_id, answer, time_spent_seconds, was_flagged}`
- `POST /api/v1/attempts/{attemptId}/complete` — финализация → результат
- `GET /api/v1/attempts/history` — история
- `GET /api/v1/explanations/{questionId}` — explanation
- `GET /api/v1/explanations/{questionId}/versions` — версии
- `POST /api/v1/explanations/telemetry/batch` — телеметрия просмотров
- `GET /api/v1/labs?track_id=` — список лаб
- `GET /api/v1/labs/{labId}` — детали лабы
- `GET /api/v1/labs/active` — активные сабмишены user'а
- `POST /api/v1/labs/start` — `{lab_id, mode}` → LabSubmission (с `devices[].terminal_ws_url`)
- `GET /api/v1/labs/submissions/{submissionId}` — состояние сессии (проверяет владельца → 403 при чужой)
- `POST /api/v1/labs/submissions/{submissionId}/stop` — остановить
- `POST /api/v1/labs/submissions/{submissionId}/pause` / `/resume`
- `POST /api/v1/labs/submissions/{submissionId}/submit-module` — `{module_number}` → автогрейдинг
- `GET /api/v1/labs/submissions/{submissionId}/scores` — LabScore[] (проверяет владельца)
- `GET /api/v1/quick-labs?track_id=` / `GET /api/v1/quick-labs/{labId}`
- `GET /api/v1/study/progress` / `POST /api/v1/study/progress/toggle` `{guide_id, completed}`

### WebSocket (auth via Bearer header или `?token=`)
- `/ws/...` — SSH proxy (терминалы) + sandbox shell

### Доменные типы — см. `backend/internal/domain/*.go`

---

## 7. Frontend — целевые требования (Фаза 2, P1)

### 7.1 Error boundaries / Loading (F9 → fix)
- `frontend/app/error.tsx` — глобальный error boundary
- Локальные `error.tsx` в `/exam`, `/labs`
- `frontend/app/loading.tsx` — skeleton
- `<Suspense>` вокруг тяжёлых chunks

### 7.2 TanStack Query (F4 → fix) — фундамент для §7.3–7.5
- `npm i @tanstack/react-query`
- `QueryClientProvider` в `app/layout.tsx`
- Заменить ручной `fetch`+`useEffect` на `useQuery`/`useMutation` во всех `lib/api.ts` клиентах
- Сохранить `lib/api.ts` как низкоуровневый транспорт; типы вынести в `frontend/lib/types.ts`

### 7.3 Версионная консистентность
- Next.js целевой — **15.2.4** (источник правды = CLAUDE.md)

### 7.4 PWA (F6 → fix)
- `frontend/public/manifest.json` + иконки (192/512)
- Service worker (`next-pwa` или ручной `sw.js`)
- Offline-fallback для `/study`

### 7.5 Server Components (F1 → fix)
- Перевести read-only страницы на RSC: landing (`/`), `/exams` catalog, `/study`
- `'use client'` оставить только интерактиву

### 7.6 Доступность a11y (F10 — ✅ частично пофикшено)
- CSS focus rule — ПОФИКШЕНО: `globals.css:354-357` имеет `outline: 2px solid var(--color-emerald-500); outline-offset: 2px;`
- TODO: `role`, `aria-label` на всём интерактиве; skip-link в `app/layout.tsx`; проверка axe-core

### 7.7 Тесты фронтенда (Фаза 1.4)
- Vitest + React Testing Library + @testing-library/user-event
- Покрыть критичные хуки: useAuth, useQuery-обёртки над API
- Playwright для smoke E2E (опционально)

### 7.8 Прочие находки
- **Типобезопасность:** `lib/api.ts` возвращает `any`/`any[]` — создать `frontend/lib/types.ts` с типами из `backend/internal/domain/*.go`
- ✅ **Дублирующий маршрут `/exam/[id]`** — удалён (2026-08-04)
- **`auth-context.tsx:48-53`:** `fetchProfile()` молча килует ошибку — различать сетевую ошибку vs 401

---

## 8. Frontend соглашения по коду
- **TypeScript strict** (`strict: true`), `@/*` path aliases
- Компоненты в `frontend/components/`, страницы в `frontend/app/`
- До push: `npm run lint` (eslint-flat config: next/core-web-vitals + @typescript-eslint)
- i18n: ключи добавлять в **оба** файла — `lib/i18n/locales/en.ts` и `ru.ts`
- UI-компоненты: manual shadcn-паттерн (CVA variants + `cn()` из `lib/utils.ts`). НЕ запускать `npx shadcn-ui add`
- Иконки: prefer @phosphor-icons/react (weight="regular"/"fill"/"light"); lucide-react для недостающих
- Motion: `framer-motion` через обёртки `components/motion/*` + `lib/motion.ts` (variants)
- Tailwind v4: `@theme` в `globals.css`, dark mode через `next-themes` (`attribute="class"`, `defaultTheme="dark"`)
- Карточки: `BentoCard` из `components/ui/card.tsx`
- Layout-обёртка: `PageShell` + `PageHeader` из `components/layout/page-shell.tsx`
- Auth-защита страницы: либо `withAuth` HOC, либо ручная проверка `useAuth()` + `router.push("/auth/login")` в useEffect
- API-вызовы: через `lib/api.ts` (`authApi`, `tracksApi`, `examsApi`, `attemptsApi`, `explanationsApi`, `labsApi`, `quickLabsApi`, `studyProgressApi`)
- WebSocket (`/ws/...`): передавать `?token=${localStorage.getItem("access_token")}` в URL

---

## 9. Backend соглашения по коду
- Clean Architecture слои: `domain/` → `repository/postgres/` → `usecase/` → `delivery/`
- До push: `golangci-lint run` (конфиг `.golangci.yaml`: govet, errcheck, staticcheck, gosec, revive, goimports)
- Struct tags: `json:"snake_case"` для API, `db:"snake_case"` для DB
- Ошибки: sentinel-ошибки domain (`ErrNotFound`, `ErrForbidden`, `ErrConflict`, `ErrValidation`) — НЕ сырой `err.Error()` в ответах
- **TODO §3:** единый маппер domain-error → HTTP-status в middleware/handler
- Тесты: `go test ./...` — стремиться к покрытию нового кода. `lab_usecase.go` — 0 unit-тестов (security-critical) — приоритет.

---

## 10. Контент — соглашения
- Вопросы: **100% оригинальные**, из публичных blueprint. Никакого braindump/NDA-контента. `content_hash` audit trail обязателен.
- Генерация: Python в `scripts/generators/` (`common.py` с `make_single_choice`/`make_multiple_choice`/..., `random.Random(seed)` для воспроизводимости)
- Экзамены (фактически реализованы — контент есть только для 4):
  - `200-301` CCNA — `generators.ccna:generate_ccna` → `077_ccna_quality_questions.sql`
  - `JN0-106` JNCIA-Junos — `generators.junos:generate_jncia_junos` → `078_...`
  - `JN0-649` JNCIP-ENT — `generators.jncip:generate_jncip_ent` → `079_...`
  - `JN0-663` JNCIP-SP — `generators.jncip:generate_jncip_sp` → `080_...`
- Лендинговые «7 треков» → уточнять «available now» vs «roadmap» для остальных 3 (JNCIE, CCNP, CCIE — нет контента)
- SQL: dollar-quoting `$$...$$`, обёртка `-- +goose StatementBegin`/`StatementEnd`, `unique_questions` per exam
- Лаб-конфиги: `backend/labs/micro-labs/` — следовать структуре существующих (01-junos-cli-basics … 05-mpls-lsp). Подробно — `backend/labs/LAB_METHODOLOGY.md`

---

## 11. Запуск и разработка

### Полный стек (нативный, без Docker)
```bash
# 1. Clone & Configure
git clone <repo-url>
cd NetCert
cd backend && cp .env.example .env

# 2. Setup Database (one-time)
sudo postgresql-setup --initdb  # Fedora
sudo systemctl enable --now postgresql redis
sudo -u postgres psql -c "CREATE USER netcert WITH PASSWORD 'netcert';"
sudo -u postgres psql -c "CREATE DATABASE netcert OWNER netcert;"
sudo -u postgres psql -c "GRANT ALL PRIVILEGES ON DATABASE netcert TO netcert;"
sudo -u postgres psql -d netcert -c "CREATE EXTENSION IF NOT EXISTS \"uuid-ossp\";"

# 3. Run Migrations
cd backend
go install github.com/pressly/goose/v3/cmd/goose@latest
export PATH=$PATH:$(go env GOPATH)/bin
goose -dir migrations postgres "postgresql://netcert:netcert@127.0.0.1:5432/netcert?sslmode=disable" up

# 4. Start Services (two terminals)
# Terminal 1 — Backend
cd backend && go run ./cmd/server/
# API: http://localhost:8080

# Terminal 2 — Frontend
cd frontend && npm ci && npm run dev
# UI: http://localhost:3000
```

### Access Points
| URL | Description |
|-----|-------------|
| `http://localhost:3000` | Landing page |
| `http://localhost:3000/auth/register` | Sign up |
| `http://localhost:3000/auth/login` | Sign in |
| `http://localhost:3000/dashboard` | Dashboard |
| `http://localhost:3000/exams` | Exam catalog |
| `http://localhost:8080/health` | API health check |

### Useful Commands
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
```

---

## 12. Источники и ссылки
- `README.md` — quick start для людей
- `CONTRIBUTING.md` — как контрибьютить (Conventional Commits, стили)
- `CODE_OF_CONDUCT.md` — Contributor Covenant
- `backend/labs/LAB_METHODOLOGY.md` — лабораторная архитектура, cRPD/vMX/vSRX/XRv9k, Containerlab
- `.github/` — CI workflow, issue/PR-templates
- `AGENTS.md` — инструкции для AI-агентов по вопрос-генерации

**Лицензия:** AGPL-3.0 (см. `LICENSE`).

---