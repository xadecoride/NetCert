# NetCert — Технический аудит

**Дата:** 2026-07-17
**Аудитор:** ZCode (анализ кодовой базы + сверка с восстановленными `AUDIT_REPORT.md`, `DEEP_AUDIT_RESULTS.md`, `AUDIT_QUESTIONS_LABS.md`, `frontend-audit-results.json`)
**Объект:** репозиторий `github.com/xadecoride/NetCert`, ветка `main`
**Верификация:** критические уязвимости подтверждены прямым чтением исходников (file:line приведены актуальные на момент аудита)

> Все находки ранжированы: 🔴 Critical/High · 🟡 Medium · 🟢 Low/Good. Ремедиация — в `ROADMAP_DEV.md`.

---

## 0. Технологический стек

| Слой | Технология | Заметка |
|---|---|---|
| Backend | **Go 1.25.7**, Chi v5.1.0, pgx/v5.9.2, pgxpool | README говорит «Go 1.22+», фактически 1.25.7 — doc drift |
| Миграции | **goose v3.20.0**, SQL-файлы через `embed.FS`, auto-apply на старте | Хорошо: фиксит login-500 на свежих БД |
| Auth | **golang-jwt/v5** (HS256 access+refresh), **bcrypt** DefaultCost | Refresh-токены выпускаются, но не используются (см. §1.4) |
| WebSocket | **gorilla/websocket v1.5.3** (терминалы лаб + stream топологии) | Эндпоинты публичны (см. §1.2) |
| SSH | **golang.org/x/crypto/ssh** | `InsecureIgnoreHostKey()` — MITM-риск (см. §3) |
| Tests | testify v1.11.1 + pgxmock/v5 | Только backend, 10 файлов |
| Frontend | **Next.js ^15.2.4** (не 16, как в PLAN), React 19, TS 5.7 strict, Tailwind v4 | App Router, но все страницы `'use client'` |
| UI | CVA+clsx+tailwind-merge (manual shadcn), lucide/phosphor/radix icons | shadcn не инициализирован через CLI |
| Terminal | @xterm/xterm v6 + addons fit/webgl | Работает |
| Topology | @xyflow/react v12 | Работает |
| Charts | recharts v2.15.0 | Установлен, почти не используется |
| Infra | Postgres 16-alpine, Redis 7-alpine, Docker Compose, **Containerlab v0.75.0** + DinD | cRPD/FRR топологии |
| Python toolchain | scripts/ + DinD | **Нет lockfile** (pyproject/requirements) |
| CI | **Отсутствует** | Нет `.github/workflows` и т.д. |

---

## 1. 🔴 Критические уязвимости (Безопасность)

### 1.1 IDOR на лаб-сабмишенах

**Файлы:** `backend/internal/delivery/http/lab_handler.go`
- `GetSubmission` (~стр. 101)
- `GetScores` (~стр. 211)

**Проблема:** хендлеры парсят `submissionId` из URL и сразу вызывают `h.labUC.GetSubmission/GetScores(ctx, id)` **без проверки владельца**. Любой залогиненный пользователь может перебирать UUID и читать чужие сабмишены и оценки.

**Контраст:** `StopLab` / `PauseLab` / `ResumeLab` / `SubmitModule` в usecase-слое **корректно** проверяют `sub.UserID != userID` — то есть это не системный недосмотр, а именно пропуск в двух read-методах.

**Ремедиация:** либо проверка `submission.UserID == userID` в usecase-методах, либо отдельный `GetSubmissionForUser(ctx, id, userID) error`. См. ROADMAP Фаза 0.

### 1.2 Неаутентифицированный WebSocket-shell

**Файл:** `backend/internal/delivery/http/router.go:57`
```go
// Lab WebSocket endpoints (public for now; will add auth later)
r.Route("/ws", func(r chi.Router) {
    sshProxy.RegisterRoutes(r)
    sandboxHandler.RegisterRoutes(r)
})
```

**Проблема:** блок `/ws` смонтирован **вне** группы `r.Use(authMw.Authenticate)` (которая начинается ниже, на строках 84+). Любой, кто знает URL, получает интерактивный shell в sandbox или лаб-устройство без JWT.

**Ремедиация:** вынести `/ws/*` под `authMw.Authenticate` + проверять владельца сабмишена для `/ws/lab/{id}`. Передача токена в WS — через query-param `?token=` или под-протокольный заголовок (см. ROADMAP Фаза 0).

### 1.3 `StopLab` продолжает исполнение после 401

**Файл:** `lab_handler.go`, метод `StopLab`
```go
userID := middleware.GetUserID(r.Context())
if userID == uuid.Nil {
    writeJSON(w, http.StatusUnauthorized, ...)   // ← нет return!
}
// дальнейший код выполнится даже при неавторизованном запросе
```

**Проблема:** missing `return` после записи 401 — последующая логика StopLab отрабатывает с `userID == uuid.Nil`. Повсюду в этом файле тот же паттерн корректно закрыт `return`, здесь — пропущено.

**Ремедиация:** добавить `return`. Тривиальный однострочный фикс.

### 1.4 Refresh-токены выпускаются, но endpoint отсутствует

**Файлы:** `backend/internal/usecase/auth_usecase.go` (генерация refresh), `backend/internal/delivery/http/router.go` (нет `/auth/refresh`)

**Проблема:** при логине refresh-токен возвращается клиенту и хранится в `localStorage`, но:
- нет эндпоинта `/auth/refresh`
- нет storage/блэклиста (Redis/DB) для refresh-токенов
- нет инвалидации

→ Refresh-токен **бесполезен** для пользователя, но **расширяет surface token-theft** (если утечёт — им нельзя воспользоваться, но он хранится и пересылается). Это «потенциальная дыра», которая сегодня не эксплуатируется, но вводит в заблуждение.

**Ремедиация (варианты):**
- (A) **Быстро:** убрать refresh из ответа `/auth/login` + убрать поле из клиента ДО реализации endpoint.
- (B) **Полноценно:** реализовать `/auth/refresh` с rotation + Redis-блэклист (как требует OWASP). ROADMAP Фаза 1.

### 1.5 Декоративные `validate:` теги

**Файл:** `backend/internal/domain/*.go` — `RegisterRequest{Email, Password, DisplayName}` и др. с тегами `validate:"required,email"`, `min=8` и т.д.

**Проблема:** теги объявлены, но `validator.Validate.Struct()` **нигде не вызывается** (grep по `validator.New` / `.Struct(` — 0 совпадений в рантайм-пути). → Регистрация принимает пустые email и пароли в 1 символ (БД всё равно спасает `NOT NULL`/`VARCHAR(100)`, но не форматы email / минимальную длину пароля).

**Ремедиация:** подключить `github.com/go-playground/validator/v10`, вызывать `.Struct(req)` в начале каждого хендлера. ROADmap Фаза 0.

---

## 2. 🔴 Инженерия / технический долг

### 2.1 Скомпилированный бинарник в git

**Файл:** `backend/server` — **34 MB Go-бинарник закоммичен** и **не в .gitignore** (там есть только `backend/bin/`). Это навсегда раздувает историю git.

**Ремедиация:** `git rm --cached backend/server` + добавить в `.gitignore` + (опц.) `git filter-repo` для очистки истории при ближайшей возможности.

### 2.2 Нет CI/CD

В репозитории **нет** `.github/workflows/`, `.gitlab-ci.yml`, `Jenkinsfile`, `.circleci/`. Каждый PR идёт без проверок.

**Ремедиация:** минимальный GitHub Actions — `go build / go vet / go test ./...`, `npm ci && npm run build`, frontend lint. ROADMAP Фаза 1.

### 2.3 Нет lint/format-конфигов и pre-commit

- Frontend: `eslint ^9.16.0` установлен, но **нет `eslint.config.*`** → `next lint` работает только на дефолтах Next.
- Backend: нет `golangci-lint` конфига, нет `goimports`/`gofumpt` энфорсмента.
- Python: нет `ruff`/`black`/`flake8`.
- Нет `.pre-commit-config.yaml`, нет Husky.

### 2.4 Тестовое покрытие

| Слой | Покрытие | Заметка |
|---|---|---|
| Backend unit | ~10 файлов (auth, exam, study_progress, user_repo) | Норм для MVP |
| **`lab_usecase.go`** | **0 unit-тестов** | Самый сложный и security-critical модуль — только `tests/integration/lab_e2e_test.go` |
| Frontend | **0 тестов** | Нет ни одного `*.test.ts(x)`, нет Vitest/Jest/Playwright |
| `quick_lab`, `explanation` usecase | 0 | |
| WS handlers, jwt manager, hash, middleware | 0 | |

### 2.5 Утечка `err.Error()` клиентам

`lab_handler.go` (стр. 93, 136, 158, 180, 203), `exam_handler.go` (148, 165) — отдают сырой `err.Error()` в JSON-ответе. Глобальный `Recoverer` есть (хорошо), но конкретные хендлоры протекают.

**Ремедиация:** типизированные ошибки домена → маппинг в HTTP-коды без раскрытия внутренностей. ROADMAP Фаза 1.

### 2.6 Гигантские SQL-файлы в репозитории

- `backend/migrations/028_v6_questions.sql` — **~16 MB**
- `backend/migrations/archive/021-027` — **~75 MB суммарно**
- `077_ccna_quality_questions.sql` — ~1.1 MB

Сгенерированный контент в дереве приложения — раздувает клон и pull. Решение Фазы 1: переместить контент в отдельный data-репозиторий / object storage, миграции оставить только схемные.

---

## 3. 🟡 Прочие security/infra-замечания (Medium)

| # | Замечание | Контекст |
|---|---|---|
| M1 | `ssh.InsecureIgnoreHostKey()` в `ssh_proxy.go:184` | MITM-риск; в аудите оценён как acceptable для эфемерных лаб, но требует явной документации и ideally ограниченного scope |
| M2 | Privileged-контейнеры: `clab-dind` (`privileged: true`, exposes `12376:2376`), `frr` (`privileged: true`) | Норм для single-tenant self-host, **опасно для multi-tenant** деплоя |
| M3 | Монтирование host Docker socket в backend (staging compose) | Container-escape risk с высоким blast radius |
| M4 | `Dockerfile.sandbox` на `alpine:latest`, `Dockerfile.dind` использует `apk --allow-untrusted` | Непин versions; drift risk |
| M5 | `frrouting/frr:latest` unpinned | Будет дрейфить, ломать воспроизводимость лаб |
| M6 | Слабые дефолт-секреты в `.env.example` / compose (`JWT_SECRET=netcert-dev-secret-change-in-production`) | **Смягчено** guard'ом в `config.go:49-60` (fail-fast в проде) — это хороший паттерн |
| M7 | `domain.Lab` vs `micro_labs` schema mismatch | Исправлен миграцией `065` (подтверждено на диске) |

---

## 4. 🟡 Frontend-проблемы

Источник: `frontend-audit-results.json` (на диске, 2026-06-13) + проверка.

| # | Чек | Статус | Комментарий |
|---|---|---|---|
| F1 | Next.js App Router + RSC | **PARTIAL** | App Router есть, но все 10 страниц `'use client'`, 0 Server Components |
| F2 | TS strict mode | **PASS** | `strict: true`, `@/*` aliases |
| F3 | Tailwind v4 + shadcn | **PARTIAL** | Tailwind v4 + `@theme`, но shadcn не через CLI, ручная CVA |
| F4 | **TanStack Query** | **FAIL** | Не установлен; ручной `fetch` + useState/useEffect |
| F5 | i18n | **PASS** | Кастомный context en/ru, `/study` и `/dashboard` локализованы |
| F6 | **PWA / Service Workers** | **FAIL** | Нет manifest/sw.js/registration |
| F7 | xterm.js | **PASS** | LabTerminal с WS, dynamic import, resize, reconnect |
| F8 | Recharts/nivo | **PARTIAL** | recharts v2.15 установлен, используется только в dashboard; @nivo не установлен |
| F9 | **Error boundaries / Loading** | **FAIL** | Нет `error.tsx` / `loading.tsx` / Suspense |
| F10 | Accessibility (WCAG) | **PARTIAL** | focus-visible в button, 1 aria-label, 0 role, нет skip-links, невалидное CSS-правило (`ring` вместо `outline`) |

**Доп. дрейф:** установлен Next.js `^15.2.4`, PLAN требует 16. Нужен единый источник правды.

---

## 5. 🟢 Что уже хорошо (положительные сигналы)

Эти пункты показывают, что базовая инженерная культура на месте:

- **Clean Architecture** строго выдержана: `domain` (чистые сущности + интерфейсы репозиториев) → `repository/postgres` → `usecase` → `delivery/http|ws`. DI через интерфейсы, что позволяет mock-тестирование.
- **JWT fail-fast guard** (`config.go:49-60`): сервер отказывается стартовать с известными небезопасными секретами в не-dev окружениях — модельный паттерн.
- **Метод подписи JWT явно pinned к HMAC** (`jwt.go:66-68`) — блокирует `alg:none`-атаку.
- **Non-root Docker users**: `appuser` (UID 1000) в backend, `nextjs` (UID 1001) в frontend.
- **Structured logging** через `log/slog` (JSON в stdout) — миграция с `log` завершена (main.go, lab_usecase.go, ssh_proxy.go, sandbox.go).
- **Миграции встроены** (`embed.FS` + goose auto-Up) — это и решило login-500.
- **Анти-enumeration**: одинаковый `ErrInvalidCredentials` для «user not found» и «wrong password».
- **xterm + React Flow** терминалы и просмотр топологии — работают end-to-end.
- **Корректные индексы** добавлены миграцией `064` (`attempts(user_id,exam_id)`, `questions(exam_id,difficulty)`).
- **Чистка контента** миграцией `063` (деактивировано 320 битых + 28 дубликатов; 9 150 активных).

---

## 6. Гигиена репозитория

| Артефакт | Где | Проблема |
|---|---|---|
| 34 MB `backend/server` | `backend/server` | Закоммичен, не в `.gitignore` |
| `test_ws.go` | корень репо | Стрей-файл одноразового теста WS-клиента |
| `session_474e1262-*.zip`, `session_extract/` | корень | AI-session-артефакты; `.gitignore` ссылается на **другое** имя zip — правило не матчит |
| `skills-lock.json` | корень | Bookkeeping плагина ZCode, не часть продукта |
| `package.json` / `package-lock.json` | корень | Только hoisted xterm/xyflow deps — странный root-манифест |
| `.gitignore` перечисляет `PLAN.md`, `CLAUDE.md`, `AUDIT_*.md` | — | Намеренно скрытые планировочные доки; ок для приватного планирования |
| История коммитов | git log | Сообщения «update», нет Conventional Commits, нет тегов версий |
| `migrations/archive/` ~75 MB | backend | Legacy-контент в дереве приложения |

---

## 7. Резюме технического состояния

**Архитектурный фундамент крепкий** (Clean Architecture, embed-миграции, slog, non-root, JWT-guard). Основные проблемы — не в дизайне, а в **незакрытых security-дырах и отсутствии инженерных обвязок** (CI, линтеры, тесты на рисковом коде, гигиена репозитория).

**Топ-5 к исправлению (подробности в `ROADMAP_DEV.md` Фаза 0–1):**
1. 🔴 IDOR на lab-submissions (`lab_handler.go`)
2. 🔴 Public WS-shell (`router.go:57`)
3. 🔴 `StopLab` missing `return` + неподключённый validator
4. 🔴 Refresh-токены без endpoint (убрать или реализовать)
5. 🔴 Убрать `backend/server` из git + завести CI/линтеры/тесты на lab_usecase

Эти пять пунктов — **предварительное условие для любого публичного деплоя**, даже в free-модели. Без них выкладывать инстанс в сеть нельзя.
