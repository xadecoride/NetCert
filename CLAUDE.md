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

## 2. Бизнес-модель

**Free / Open Source навсегда. Без платных тиров.** Решение владельца, зафиксировано в AUDIT_BUSINESS.md §3.2 и дорожной карте. В коде нет ни одной платёжной интеграции. Все формулировки «Premium / подписки» в историческом PLAN.md считаются superseded.

Лендинговый copy НЕ должен содержать:
- «1,200+ Active learners» — недоказуемо (нет аналитики). Заменять на «Self-hostable / Open Source».
- «AI-adaptive / FSRS» — не реализовано (атtemtы используют `math/rand`). Убрать или реализовать (Фаза 3.1).
- Противоречивые числа вопросов («9,150+» vs «1,200+ original») — сводить к одному источнику (live-запрос к БД / константа).

## 3. Текущая фаза разработки

| Фаза | Статус | Замечание |
|------|--------|-----------|
| **0. Hotfix безопасности (P0)** | ✅ закрыта | IDOR-stop, WS auth, validator, refresh-token removal |
| 0.3 — ownership-проверка в `ws/ssh_proxy.go handleTerminal` | ⏳ TODO | auth есть, ownership нет |
| **1. Фундамент качества (P1)** | частично | CI, линтеры, гигиена ✅ ; тесты lab_usecase, единый error-маппер, контент-вне-git — TODO |
| **2. Frontend cleanup (P1)** | 🔴 НЕ НАЧАТА | целевая зона для frontend-работы (см. §7) |
| 3. Продуктовый parity (P2) | backlog | FSRS, честный copy, recharts-визуализации |
| 4. OSS-зрелость (P2) | частично | LICENSE/CONTRIBUTING/CODE_OF_CONDUCT/PR-templates ✅; README-бейджи, Telegram, prod-deploy — TODO |

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
- **Next.js ^15.2.4** (не 16 — зафиксировано как целевое; §8 про версионность)
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
- PostgreSQL 16-alpine, Redis 7-alpine, Docker Compose
- Containerlab v0.75.0 + DinD (cRPD/FRR топологии; cRPD требует Juniper license)
- Non-root Docker users (appuser UID 1000 в backend, nextjs UID 1001 в frontend)
- CI: `.github/workflows/ci.yml` — matrix backend (go build/vet/test) + frontend (npm ci/lint/build)

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
- JWT fail-fast guard в `config.go:49-60` ( сервер отказывается стартовать с небезопасными секретами в не-dev окружениях).
- JWT подпись явно pinned к HMAC — блокирует `alg:none`-атаку (`jwt.go:66-68`).
- Анти-enumeration на login: одинаковый `ErrInvalidCredentials` для «user not found» и «wrong password».
- WS endpoints (`/ws/*`) — под `authMw.AuthenticateWS` (Bearer header или `?token=` query param). **TODO §3: проверка владельца сабмишена в ssh_proxy.handleTerminal.**
- Структурированный лог: `slog` JSON в stdout, не `log`.

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

## 6. API-контракт (актуальный — `backend/internal/delivery/http/router.go`)

### Public
- `GET /health` → `{"status":"ok","version":"1.0.0"}`
- `POST /api/v1/auth/register` — body `{email, password, display_name}` → `{user, access_token, expires_in}` (валидация `required,email` / `required,min=8` / `required,min=2,max=100`)
- `POST /api/v1/auth/login` — body `{email, password}` → `{user, access_token, expires_in}`
- `GET /api/v1/tracks` — список треков
- `GET /api/v1/tracks/{slug}` — детали трека
- `GET /api/v1/tracks/{slug}/exams` — экзамены трека
- `GET /api/v1/sandbox/status` — health sandbox (не чувсвт.)

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
- `/ws/...` — SSH proxy (терминалы) + sandbox shell (см. `ws.RegisterRoutes`)

### Доменные типы — см. `backend/internal/domain/*.go`
- `User`: `{id, email, display_name, role, avatar_url?, oauth_provider?, oauth_id?, is_email_verified, streak_days, total_xp, preferences?, created_at, updated_at}`. `password_hash` — `json:"-"`.
- `Track`: `{id, slug, vendor: juniper|cisco, name, description, icon_url?, sort_order, created_at}`
- `Exam`: `{id, track_id, code, name, level: JNCIA|JNCIP|JNCIE|CCNA|CCNP|CCIE, duration_minutes, total_questions, passing_score, blueprint_url?, is_active, created_at}`
- `Attempt`: `{id, user_id, exam_id, status: in_progress|paused|completed|timed_out|abandoned, mode, started_at, completed_at?, duration_seconds, score?, questions_total, questions_answered, questions_correct, questions_flagged?, created_at}`
- `AttemptWithDetails`: Attempt + `{exam_name?, exam_code?, passing_score?, questions: AttemptQuestionWithAnswer[]}` где каждый вопрос `{id, body, options?, question_type, difficulty, explanation, reference_urls?, blueprint_section, user_answer, is_correct, was_flagged, time_spent_seconds}`
- `Lab`: `{id, track_id, slug, title, description, level, duration_minutes, topology_yaml?, initial_configs?, task_description, grading_script?, fault_config?, is_troubleshooting, technology, max_score, passing_score, num_devices, lab_directory, is_active, created_at, updated_at}`
- `LabSubmission`: `{id, lab_id, user_id, status: pending|deploying|running|paused|completed|failed|timed_out, pod_id, devices?: LabDevice[], started_at, completed_at?, time_remaining_seconds, current_score, max_score, snapshot_id?, topology_update_url?, terminal_ws_url?, created_at}`. `LabDevice`: `{name, kind, mgmt_ip, ssh_port, status, interfaces?}`.
- `LabScore`: `{id, submission_id, module_number, module_title, task_score, max_score, scoring_output?: ScoringCheck[], is_autograded, created_at}`. `ScoringCheck`: `{command, expected_match, actual_output, passed, points_awarded, max_points}`.

## 7. Frontend — целевые требования (Фаза 2, P1)

Из `AUDIT_TECHNICAL.md §4` + `ROADMAP_DEV.md Фаза 2`. Это основная зона frontend-работы.

### 7.1 Error boundaries / Loading (F9 → fix)
- `frontend/app/error.tsx` — глобальный error boundary
- Локальные `error.tsx` в `/exam`, `/labs`
- `frontend/app/loading.tsx` — skeleton
- `<Suspense>` вокруг тяжёлых chunks

### 7.2 TanStack Query (F4 → fix) — фундамент для §7.3–7.5
- `npm i @tanstack/react-query`
- `QueryClientProvider` в `app/layout.tsx`
- Заменить ручной `fetch`+`useEffect` на `useQuery`/`useMutation` во всех `lib/api.ts` клиентах (auth, tracks, exams, attempts, explanations, labs, quickLabs, studyProgress)
- Сохранить `lib/api.ts` как низкоуровневый транспорт; типы вынести в `frontend/lib/types.ts` (см. §8)

### 7.3 Версионная консистентность (фикс в этом файле §4)
- Next.js целевой — **15.2.4** (источник правды = CLAUDE.md). Обновить README/PLAN при расхождении.
- README упомянал «Next.js 16» — это устаревшее, правки внесены в §4.

### 7.4 PWA (F6 → fix)
- `frontend/public/manifest.json` + иконки (192/512)
- Service worker (`next-pwa` или ручной `sw.js`)
- Offline-fallback для `/study`

### 7.5 Server Components (F1 → fix)
- Перевести read-only страницы на RSC: landing (`/`), `/exams` catalog, `/study`
- `'use client'` оставить только интерактиву (формы auth, экзамен, терминал, топология, dashboard widgets)

### 7.6 Доступность a11y (F10 — ✅ частично пофикшено в коде)
- ~~CSS focus rule~~ — ПОФИКШЕНО: `frontend/app/globals.css:354-357` имеет корректное `outline: 2px solid var(--color-emerald-500); outline-offset: 2px;`. `header.tsx` и др. используют `focus-visible:outline-*`. Пункт F10 о «ring вместо outline» — устарел.
- TODO: `role`, `aria-label` на всём интерактиве; skip-link в `app/layout.tsx`; проверка axe-core (можно как dev-зависимость)

### 7.7 Тесты фронтенда (Фаза 1.4)
- Vitest + React Testing Library + @testing-library/user-event
- Покрыть критичные хуки: useAuth, useQuery-обёртки над API
- Playwright для smoke E2E (опционально)

### 7.8 Прочие находки (мой анализ кода)
- **Типобезопасность:** `lib/api.ts` возвращает `any`/`any[]` — слабая типизация. Создать `frontend/lib/types.ts` с типами, отражающими `backend/internal/domain/*.go`. Это предпосылка для качественного TS strict.
- ~~**Дублирующий маршрут `/exam/[id]`**~~ — ✅ удалён (2026-08-04). Был stale-копией `/exams/[id]/` (642 vs 460 строк, single-quotes, без вынесенных компонентов). Роут-проверки в `header.tsx:49` и `mobile-nav.tsx:27` перенесены с `/exam/` на `/exams/`.
- **`auth-context.tsx:48-53`:** `fetchProfile()` молча килует ошибку — различать сетевую ошибку vs 401 (при 401 чистить токен; при retryable ошибки сети — оставить user'а).

## 8. Frontend соглашения по коду

- **TypeScript strict** (`strict: true`), `@/*` path aliases (`@/components/...`, `@/lib/...`)
- Компоненты в `frontend/components/`, страницы в `frontend/app/`
- До push: `npm run lint` (eslint-flat config в `frontend/eslint.config.js`: next/core-web-vitals + @typescript-eslint)
- i18n: ключи добавлять в **оба** файла — `lib/i18n/locales/en.ts` и `ru.ts`
- UI-компоненты: manual shadcn-паттерн (CVA variants + `cn()` из `lib/utils.ts`). НЕ запускать `npx shadcn-ui add` — в проекте нет shadcn CLI, компоненты ручные.
- Иконки: prefer @phosphor-icons/react (weight="regular"/"fill"/"light"); lucide-react для недостающих; @radix-ui/react-icons редко
- Motion: `framer-motion` через обёртки `components/motion/*` (KineticMarquee, MagneticButton, SectionReveal, SpotlightCard, TextScramble, AnimatedCounter) + `lib/motion.ts` (variants)
- Tailwind v4: `@theme` в `globals.css`, dark mode через `next-themes` (`attribute="class"`, `defaultTheme="dark"`)
- Карточки: `BentoCard` из `components/ui/card.tsx` (НЕ plain `Card`)
- Layout-обёртка: `PageShell` + `PageHeader` из `components/layout/page-shell.tsx`
- Auth-защита страницы: либо `withAuth` HOC, либо ручная проверка `useAuth()` + `router.push("/auth/login")` в useEffect
- API-вызовы: через `lib/api.ts` (`authApi`, `tracksApi`, `examsApi`, `attemptsApi`, `explanationsApi`, `labsApi`, `quickLabsApi`, `studyProgressApi`). НЕ `fetch` напрямую в страницах.
- WebSocket (`/ws/...`): передавать `?token=${localStorage.getItem("access_token")}` в URL (см. `LabWorkspace.tsx`)

## 9. Backend соглашения по коду

- Clean Architecture слои: `domain/` → `repository/postgres/` → `usecase/` → `delivery/`
- До push: `golangci-lint run` (конфиг `.golangci.yaml`: govet, errcheck, staticcheck, gosec, revive, goimports)
- Struct tags: `json:"snake_case"` для API, `db:"snake_case"` для DB
- Ошибки: sentinel-ошибки domain (`ErrNotFound`, `ErrForbidden`, `ErrConflict`, `ErrValidation`) — НЕ сырой `err.Error()` в ответах
- **TODO §3:** единый маппер domain-error → HTTP-status в middleware/handler
- Тесты: `go test ./...` — стремиться к покрытию нового кода. `lab_usecase.go` — 0 unit-тестов (security-critical) — приоритет.

## 10. Контент — соглашения

- Вопросы: **100% оригинальные**, из публичных blueprint. Никакого braindump/NDA-контента. `content_hash` audit trail обязателен.
- Генерация: Python в `scripts/generators/` (`common.py` с `make_single_choice`/`make_multiple_choice`/..., `random.Random(seed)` для воспроизводимости)
- Экзамены (фактически реализованы — контент есть только для 4 из 7 заявленных):
  - `200-301` CCNA — `generators.ccna:generate_ccna` → `077_ccna_quality_questions.sql`
  - `JN0-106` JNCIA-Junos — `generators.junos:generate_jncia_junos` → `078_...`
  - `JN0-649` JNCIP-ENT — `generators.jncip:generate_jncip_ent` → `079_...`
  - `JN0-663` JNCIP-SP — `generators.jncip:generate_jncip_sp` → `080_...`
- Лендинговые «7 треков» → уточнять «available now» vs «roadmap» для остальных 3 (JNCIE, CCNP, CCIE — нет контента).
- SQL: dollar-quoting `$$...$$`, обёртка `-- +goose StatementBegin`/`StatementEnd`, `unique_questions` per exam
- Лаб-конфиги: `backend/labs/micro-labs/` — следовать структуре существующих (01-junos-cli-basics … 05-mpls-lsp). Подробно — `backend/labs/LAB_METHODOLOGY.md`.

## 11. Запуск и разработка

### Полный стек одной командой
```bash
cp backend/.env.example backend/.env
make up          # Postgres, Redis, backend (:8080), frontend (:3000); миграции авто
make down
```

### Отдельно
```bash
make dev-infra       # Postgres + Redis
make dev-backend     # http://localhost:8080
make dev-frontend    # http://localhost:3000
make migrate-up      # применить миграции
```

### Генерация вопросов
```bash
python3 scripts/generate_quality_questions.py [ccna|jncia-junos|jncip-ent|jncip-sp]
```

### Валидация вывода (in-memory, без БД)
```python
import sys; sys.path.insert(0, 'scripts')
from generators.ccna import generate_ccna
qs = generate_ccna(total=1000, seed=42)
print('Total:', len(qs))
```

### URLs (dev)
- Frontend: http://localhost:3000 (landing, /auth/register, /auth/login, /dashboard, /exams)
- API health: http://localhost:8080/health

---

## 12. Источники и ссылки

- `README.md` — quick start для людей
- `CONTRIBUTING.md` — как контрибьютить (Conventional Commits, стили)
- `CODE_OF_CONDUCT.md` — Contributor Covenant
- `backend/labs/LAB_METHODOLOGY.md` — лабораторная архитектура, cRPD/vMX/vSRX/XRv9k, Containerlab
- `.github/` — CI workflow, issue/PR-templates
- `AGENTS.md` — инструкции для AI-агентов по вопрос-генерации (исторический, дублирует часть §10)
- `AUDIT_TECHNICAL.md`, `AUDIT_BUSINESS.md`, `ROADMAP_DEV.md`, `IDEAS_INITIATIVES.md` — исторические аудиты/планы. Расхождения — трактуются в пользу CLAUDE.md.

**Лицензия:** AGPL-3.0 (см. `LICENSE`).
