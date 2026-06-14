# План исправлений ошибок по результатам аудита NetCert

## Резюме

На основании трёх аудит-файлов (`AUDIT_QUESTIONS_LABS.md`, `AUDIT_REPORT.md`, `DEEP_AUDIT_RESULTS.md`) и проверки исходного кода выявлены проблемы трёх категорий:

1. **База данных (вопросы + лабы)** — повреждённые вопросы, отсутствующие лабы, пропущенные индексы.
2. **Backend (Go)** — нарушения Clean Architecture, security gaps, отсутствие тестов.
3. **Инфраструктура (Docker)** — контейнеры запускаются от root, отсутствуют healthcheck'и.

**Важное уточнение:** `AUDIT_REPORT.md` содержит FALSE POSITIVE — `AuthUseCase` **корректно** использует интерфейс `domain.UserRepository` (строка 22 `auth_usecase.go`). Это нужно исправить в отчёте.

---

## Приоритеты

| Фаза | Приоритет | Что делаем |
|------|-----------|------------|
| 1 | CRITICAL | Миграции БД: исправить вопросы, вернуть лабы, добавить индексы |
| 2 | HIGH | DI-интерфейсы для всех репозиториев + рефактор usecases |
| 3 | HIGH | Security: JWT expiry, WS origin hardening, dev-login гейт |
| 4 | MEDIUM | Инфраструктура: non-root user, healthcheck, pinned образы |
| 5 | MEDIUM | Логирование: миграция `log` → `log/slog` |
| 6 | LOW | Тесты: unit-тесты для usecases с testify + pgxmock |

---

## Фаза 1. Исправления в БД (миграции)

### 1.1 Миграция `063_fix_questions.sql`
**Цель:** Исправить 320 вопросов с пустыми опциями + 131 вопрос с 4 correct + дубликаты.

- Деактивировать (`is_active = false`) 320 вопросов, у которых **все 4 опции имеют пустой `text`**.
- Для 131 вопроса (есть текст, но `is_correct = true` у всех 4 опций) — оставить `is_correct = true` только у **первой** опции, у остальных `false`.
- Найти и деактивировать **строгие дубликаты `body` внутри одного `exam_id`** (60 штук по данным аудита).

### 1.2 Миграция `064_add_performance_indexes.sql`
**Цель:** Добавить composite indexes для частых запросов.

```sql
CREATE INDEX IF NOT EXISTS idx_attempts_user_exam ON attempts(user_id, exam_id);
CREATE INDEX IF NOT EXISTS idx_questions_exam_difficulty ON questions(exam_id, difficulty);
```

### 1.3 Миграция `065_micro_labs.sql` (или применить `042_micro_labs.sql`)
**Цель:** Таблица `micro_labs` отсутствует в БД.

- Вариант А: Если используется `goose` — применить существующую `042_micro_labs.sql`.
- Вариант Б: Если миграции накатываются вручную — создать `065_micro_labs.sql` с `CREATE TABLE IF NOT EXISTS micro_labs` + 5 INSERT (копия из `042`).
- **Дополнительно:** добавить недостающие колонки в `micro_labs`, которые есть в `domain.Lab` но отсутствуют в схеме:
  - `max_score INT DEFAULT 100`
  - `passing_score INT DEFAULT 70`
  - `num_devices INT DEFAULT 0`

---

## Фаза 2. Clean Architecture / DI

### 2.1 Добавить интерфейсы в `backend/internal/domain/repository.go`

Добавить:
- `ExamRepository` — методы: `ListTracks`, `FindTrackBySlug`, `ListExams`, `FindExamByID`, `ListQuestions`, `ListQuestionIDs`, `GetQuestionsByIDs`, `FindQuestionByID`
- `AttemptRepository` — методы: `Create`, `FindByID`, `ListByUser`, `UpdateStatus`, `Complete`, `UpdateProgress`, `SaveAnswer`, `GetAnswers`, `SaveAttemptQuestions`, `GetAttemptQuestionIDs`, `IsQuestionInAttempt`, `HasUserAnsweredQuestion`, `HasAnswer`
- `ExplanationRepository` — методы: `FindByQuestionID`, `FindVersionByQuestionID`, `ListVersions`, `SaveTelemetryEvents`
- `StudyProgressRepository` — методы: `ListByUser`, `Upsert`

### 2.2 Обновить usecases

- `backend/internal/usecase/exam_usecase.go` — заменить `*postgres.ExamRepository` и `*postgres.AttemptRepository` на `domain.ExamRepository` и `domain.AttemptRepository`.
- `backend/internal/usecase/explanation_usecase.go` — заменить `*postgres.ExplanationRepository` и `*postgres.AttemptRepository` на интерфейсы.
- `backend/internal/usecase/study_progress_usecase.go` — заменить `*postgres.StudyProgressRepository` на интерфейс.

### 2.3 Обновить `router.go` и `main.go`

- `router.go` — принимает конкретные `*usecase.*UseCase`. Для handler-тестов желательно ввести интерфейсы usecase'ов в `delivery/http` или использовать существующие. **Минимум:** оставить как есть (usecase-структуры не мешают, если внутри них интерфейсы репозиториев).
- `main.go` — не требует изменений, т.к. конкретные репозитории реализуют новые интерфейсы.

---

## Фаза 3. Security

### 3.1 JWT Expiry (LOW → быстрый fix)
- В `auth_usecase.go` строки 73, 101, 142 заменить `ExpiresIn: 900` на `int(uc.jwtManager.AccessTokenTTL().Seconds())` (требует добавления геттера в `JWTManager` или использования `cfg.JWT.AccessTokenTTL`).

### 3.2 WebSocket Origin Check
- Уже реализовано через `ws.SetAllowedOrigins(allowedOrigins)` в `router.go:32`.
- **Доработка:** в `ssh_proxy.go` fallback `CheckOrigin: return true` для dev остаётся, но при `APP_ENV != development` и пустом `CORS_ORIGINS` нужно запрещать все origins. Добавить валидацию в `parseCORSOrigins`.

### 3.3 DevLogin
- **УЖЕ ЗАЩИЩЁН** — `router.go:79` проверяет `if appEnv == "development"`. Ничего делать не нужно, но стоит добавить логирование попыток вызова dev-login вне dev-режима.

### 3.4 SSH InsecureIgnoreHostKey
- Добавить комментарий в `ssh_proxy.go:215` с документированием риска MITM для ephemeral lab containers.

### 3.5 docker-compose.yml JWT_SECRET
- Добавить комментарий рядом с `JWT_SECRET: netcert-dev-secret-change-in-production`, что это **dev-only** значение и `config.go` блокирует запуск в production с этим секретом.

---

## Фаза 4. Инфраструктура Docker

### 4.1 `infra/Dockerfile.backend`
- Добавить перед `CMD`:
```dockerfile
RUN adduser -D -u 1000 appuser && chown -R appuser /app
USER appuser
```

### 4.2 `infra/docker-compose.yml`
- Добавить `healthcheck` для backend:
```yaml
healthcheck:
  test: ["CMD-SHELL", "wget -qO- http://localhost:8080/health || exit 1"]
  interval: 10s
  timeout: 5s
  retries: 3
```
- Добавить `APP_ENV: development` явно в environment backend.

### 4.3 `infra/Dockerfile.sandbox`
- Заменить `FROM alpine:latest` на `FROM alpine:3.19`.

---

## Фаза 5. Логирование (log → slog)

### 5.1 Постепенная миграция
- В `cmd/server/main.go` инициализировать `log/slog` с `JSONHandler`.
- Заменить все `log.Printf` в `lab_usecase.go`, `ssh_proxy.go`, `sandbox.go` на `slog.Info`/`slog.Error` с structured fields.
- **Примечание:** это крупное изменение, можно выполнять поэтапно (начать с `main.go` и `lab_usecase.go`).

---

## Фаза 6. Тесты

### 6.1 Unit-тесты для usecases
- Уже есть `testify` и `pgxmock` в `go.mod`.
- Создать:
  - `backend/internal/usecase/auth_usecase_test.go` — тесты Register/Login с моком `domain.UserRepository`.
  - `backend/internal/usecase/exam_usecase_test.go` — тесты StartAttempt/SubmitAnswer с моками `domain.ExamRepository` и `domain.AttemptRepository`.

### 6.2 Интеграционные тесты
- `backend/tests/integration/lab_e2e_test.go` уже существует. Добавить тесты для основных API-эндпоинтов (`/health`, `/tracks`, `/auth/login`).

---

## Исправления в самих файлах аудита

### `AUDIT_REPORT.md`
- **Удалить/исправить** пункт `CRITICAL: Dependency Inversion Violation` для `auth_usecase.go` — это false positive.
- **Уточнить**, что `DevLogin` уже закрыт за `APP_ENV == development`.
- Добавить найденные в DEEP_AUDIT проблемы: `ExamUseCase DI`, `ExplanationUseCase DI`, `StudyProgressUseCase DI`, `Router concrete types`.

### `DEEP_AUDIT_RESULTS.md`
- Добавить finding о несоответствии схемы `micro_labs` и `domain.Lab` (отсутствующие колонки `max_score`, `passing_score`, `num_devices`).
- Пометить `DevLogin` как FIXED в router.go (строка 79).

---

## Контрольный список завершения

- [ ] Миграция 063 (fix questions) создана и проверена
- [ ] Миграция 064 (indexes) создана
- [ ] Миграция 065 (micro_labs + schema alignment) создана
- [ ] Интерфейсы `ExamRepository`, `AttemptRepository`, `ExplanationRepository`, `StudyProgressRepository` добавлены в domain
- [ ] Все usecases рефакторены на интерфейсы
- [ ] JWT ExpiresIn использует config значение
- [ ] Dockerfile.backend запускается от non-root
- [ ] docker-compose.yml имеет healthcheck backend
- [ ] Dockerfile.sandbox использует pinned alpine:3.19
- [ ] `log` заменён на `slog` в main.go + lab_usecase.go + ssh_proxy.go
- [ ] Unit-тесты для AuthUseCase и ExamUseCase написаны и проходят
- [ ] `go test ./...` проходит без ошибок
- [ ] AUDIT_REPORT.md и DEEP_AUDIT_RESULTS.md обновлены
