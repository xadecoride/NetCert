# NetCert — План развития (Roadmap)

**Дата:** 2026-07-17 · **Принцип приоритизации:** Безопасность → Технический долг → Фичи
**Бизнес-модель:** Free / Open Source навсегда (без платных тиров)
**Источник находок:** `AUDIT_BUSINESS.md`, `AUDIT_TECHNICAL.md`

> Чек-боксы `[ ]` → `[x]` по мере выполнения. Каждая задача ссылается на конкретные файлы.

---

## Легенда приоритетов

- **P0** — критично для безопасности/честности. **Блокер публичного деплоя.**
- **P1** — фундамент качества и поддерживаемости.
- **P2** — продуктовый рост и зрелость OSS.

---

## ФАЗА 0 — Hotfix безопасности (P0, ~1–3 дня)

> Цель: закрыть 5 критических дыр из `AUDIT_TECHNICAL.md` §1. Без этого выкладывать инстанс в сеть нельзя.

### 0.1 IDOR на лаб-сабмишенах ✅
- [x] `backend/internal/usecase/lab_usecase.go` — `GetSubmission` и `GetScores` теперь принимают `userID` и проверяют `sub.UserID != userID` → `domain.ErrForbidden`. Сигнатуры handler'а пробрасывают `middleware.GetUserID(ctx)`.
- [x] `backend/internal/delivery/http/lab_handler.go` — маппинг `ErrForbidden → 403`, `ErrNotFound → 404`.
- [ ] Юнит-тест: чужой сабмишен → 403 (в очереди Фаза 1.4).

### 0.2 `StopLab` — missing `return` ✅ УЖЕ ИСПРАВЛЕНО В КОДЕ
- [x] В текущем коде `lab_handler.go` `return` присутствует. Пункт закрыт без действий.

### 0.3 WebSocket-shell без auth ✅
- [x] `backend/internal/middleware/auth.go` — добавлен `AuthenticateWS` (читает `Authorization: Bearer` или `?token=` query-param).
- [x] `backend/internal/delivery/http/router.go` — `/ws` вынесен в `r.Group(r.Use(authMw.AuthenticateWS))`. Публичный shell закрыт.
- [x] `frontend/components/lab/LabWorkspace.tsx` — `wsUrl` теперь добавляет `?token=`.
- [ ] Проверка владельца сабмишена в `ws/ssh_proxy.go` `handleTerminal` — пока проверяется только auth, не ownership (в очереди).

### 0.4 Декоративные `validate:` теги ✅
- [x] Добавлена зависимость `github.com/go-playground/validator/v10 v10.26.0` в `go.mod`.
- [x] Создан `backend/internal/pkg/validator/validator.go` — обёртка с читаемым форматом ошибок и интеграцией с `domain.ErrValidation`.
- [x] Вызовы `validator.Struct(req)` добавлены в `Register`, `Login`, `UpdateEmail` (`auth_handler.go`).

### 0.5 Refresh-токены без endpoint ✅
- [x] Убрано поле `RefreshToken` из `domain.AuthResponse` (и удалён `TokenPair`).
- [x] `auth_usecase.go` — `Register` и `Login` больше не генерируют refresh-токен.
- [x] Frontend (`auth-context.tsx`, `api.ts`) — удалено сохранение/чтение `refresh_token` из localStorage.
- [ ] (Отложено, Фаза 1) Полноценная реализация `/auth/refresh` с rotation + Redis-блэклист.

---

## ФАЗА 1 — Фундамент качества (P1, ~1–2 недели)

### 1.1 Гигиена репозитория ✅
- [x] `git rm --cached backend/server` + добавить `backend/server`, `backend/bin/` в `.gitignore`.
- [x] `.gitignore`: починить правило для `session_*.zip` (теперь матчит `session_*.zip`) + добавить `session_extract/`, `skills-lock.json`, `/test_ws.go` (или удалить эти артефакты).
- [ ] (опц.) `git filter-repo` для очистки истории от 34 MB бинарника и 75 MB archive — когда не страшно переписать историю.

### 1.2 CI/CD ✅
- [x] `.github/workflows/ci.yml`: matrix — backend (`go build`, `go vet`, `go test ./...`), frontend (`npm ci`, `npm run lint`, `npm run build`).
- [x] Кэширование `~/go/pkg/mod` и `~/.npm`.

### 1.3 Линтинг / форматирование ✅
- [x] Backend: `.golangci.yaml` (govet, errcheck, staticcheck, gosec, revive, goimports).
- [x] Frontend: `eslint.config.js` (next/core-web-vitals + @typescript-eslint).
- [x] `.pre-commit-config.yaml`: gofmt, go-vet, golangci-lint, eslint, end-of-file-fixer.
- [ ] Husky + lint-staged (frontend).

### 1.4 Тесты
- [ ] Unit-тесты для `lab_usecase.go` (через DI-интерфейсы репозиториев + pgxmock/mocks). Покрыть: StartLab, StopLab, PauseLab/ResumeLab, SubmitModule, GetSubmission (с проверкой владельца).
- [x] Тест на `validator` в auth_handler.
- [ ] Frontend: Vitest + React Testing Library на критичные хуки (useAuth, useApi).

### 1.5 Обработка ошибок
- [x] Типизированные доменные ошибки (`domain/errors.go`: `ErrNotFound`, `ErrForbidden`, `ErrConflict`, `ErrValidation`).
- [ ] Единый маппер `domain error → HTTP code` в middleware/handler. Убрать сырой `err.Error()` из ответов (lab_handler, exam_handler).

### 1.6 Контент вне git
- [ ] Перенести `028_v6_questions.sql` (16 MB) и `migrations/archive/` в отдельный data-репозиторий или object storage. Миграции оставить только схемные.

---

## ФАЗА 2 — Frontend cleanup (P1)

### 2.1 Error boundaries / Loading
- [ ] `frontend/app/error.tsx` (глобальный) + локальные в `/exam`, `/labs`.
- [ ] `frontend/app/loading.tsx` (skeleton).
- [ ] `<Suspense>` вокруг тяжёлых chunks.

### 2.2 TanStack Query
- [ ] `npm i @tanstack/react-query`, `QueryClientProvider` в layout.
- [ ] Заменить ручной `fetch`+`useEffect` на хуки `useQuery`/`useMutation` (auth, exams, attempts, labs).

### 2.3 Версионная консистентность
- [ ] Решить: поднять Next.js до 16 (как в PLAN) **или** обновить PLAN до 15.2.4. Зафиксировать единый источник правды.

### 2.4 PWA
- [ ] `frontend/public/manifest.json` + иконки.
- [ ] Service worker (`next-pwa` или ручной `sw.js`).
- [ ] Offline-fallback для страниц `/study`.

### 2.5 Server Components
- [ ] Перевести статичные страницы (landing, `/exams` catalog, `/study` read-only) на RSC. Оставить `'use client'` только интерактиву.

### 2.6 Доступность
- [ ] Починить CSS focus rule (`outline`, не `ring`).
- [ ] `role`, `aria-label` на интерактиве; skip-link; проверка axe-core.

---

## ФАЗА 3 — Продуктовый parity (P2)

### 3.1 FSRS / адаптивный выбор вопросов
- [ ] Реализовать FSRS-алгоритм (или модифицированный SM-2) в `usecase/exam` или новом `usecase/spaced_repetition`.
- [ ] Таблицы `spaced_repetition_cards`, `user_weaknesses` (уже в схеме PLAN §5).
- [ ] `StartAttempt` — взвешенный выбор вопросов по слабым зонам вместо `math/rand`.
- [ ] Либо **убрать** формулировку «AI-adaptive / FSRS» с лендинга до реализации.

### 3.2 Честность маркетинга
- [ ] Убрать «1,200+ Active learners» (`frontend/app/page.tsx`) — недоказуемо. Заменить на «Self-hostable / Open Source».
- [ ] Свести «9,150+ Questions» (`page.tsx`) и «1,200+ original questions» (`en.ts:40`) к одному числу из БД.
- [ ] Уточнить «available now» vs «roadmap» для треков.

### 3.3 Аналитика-визуализации
- [ ] Использовать Recharts: radar (Knowledge Radar), heatmap слабых зон, time-trend, readiness-индикатор. Сейчас установлен, но почти не используется.

---

## ФАЗА 4 — Бизнес / OSS-зрелость (P2)

### 4.1 Лицензия и сообщество ✅
- [x] **Добавить LICENSE** — рекомендация AGPL-3.0 (сильнее защищает free-модель от закрытого риза) или MIT (максимальный adoption).
- [x] `CONTRIBUTING.md` (как добавлять вопросы, как запускать лабы, стиль кода).
- [x] `CODE_OF_CONDUCT.md` (Contributor Covenant).
- [x] `.github/ISSUE_TEMPLATE/` (bug + feature), `.github/PULL_REQUEST_TEMPLATE.md`.
- [ ] README-бейджи: CI status, license, Telegram-чат.
- [ ] Открыть канал сообщества (Telegram-группа — естественно для RU-сегмента).
- [ ] Conventional Commits + CHANGELOG.md.

### 4.2 Production deployment
- [ ] `infra/docker-compose.prod.yml` (отдельно от staging): external secrets, образы с tag'ами.
- [ ] Reverse proxy: Caddy (auto-TLS) или Traefik + Let's Encrypt.
- [ ] `.env.production.example`, документация по домену/TLS.
- [ ] Backup Postgres (pg_dump cron / WAL-G).

### 4.3 Документация для end-user
- [ ] «Как пройти экзамен» — пошаговый гайд со скриншотами.
- [ ] «Как запустить лабу локально» (cRPD-лицензия, Docker-requirements).
- [ ] FAQ.

### 4.4 Privacy-first аналитика
- [ ] Self-hosted Plausible (для отчётности спонсорам/грантодателям) — опционально, cookieless.

### 4.5 Устойчивость free-модели
- [ ] GitHub Sponsors / Open Collective / Boosty-ссылка в README.
- [ ] Документ по стратегии compute-тяжёлых лаб: self-host-первый, ограниченный concurrency на публичном инстансе, гранты на инфру.

---

## Порядок исполнения (рекомендуемый)

```
Фаза 0 (P0, безопасность)      ── блокер публичного деплоя
  └─→ Фаза 1 (P1, качество)    ── CI, линтеры, гигиена, тесты
        └─→ Фаза 2 (P1, frontend) ── UX-паритет
              └─→ Фаза 4.1 (LICENSE+сообщество) ── можно параллельно с Фазой 0
                    └─→ Фаза 3 (P2, фичи)        ── рост
                          └─→ Фаза 4.2–4.5         ── масштаб
```

**Минимальный жизнеспособный публичный релиз:** Фаза 0 + Фаза 1.1 + Фаза 1.2 + Фаза 4.1 (LICENSE). Без LICENSE и без security-фиксов деплой бессмысленен/опасен.
