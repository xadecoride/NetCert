# NetCert 🏆

Бесплатная платформа для подготовки к сертификационным экзаменам **Juniper (JNCIA→JNCIE)** и **Cisco (CCNA→CCIE)**. Все материалы доступны после регистрации.

---

## 📋 Предварительная установка

Перед запуском убедись, что всё необходимое установлено:

### 1. Docker + Docker Compose
```bash
curl -fsSL https://get.docker.com | sudo sh
sudo usermod -aG docker $USER
# Выйди и зайди заново (или: newgrp docker)
docker --version
docker compose version
```

### 2. Go 1.22+
```bash
wget -q https://go.dev/dl/go1.22.10.linux-amd64.tar.gz
sudo rm -rf /usr/local/go
sudo tar -C /usr/local -xzf go1.22.10.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin' >> ~/.bashrc
source ~/.bashrc
go version
```

### 3. PostgreSQL клиент
```bash
sudo apt update && sudo apt install -y postgresql-client
psql --version
```

### 4. Node.js (уже установлен — v22.22.1)
```bash
node --version
npm --version
```

---

## 🚀 Полный запуск (4 шага)

Выполняй в **4 терминалах** по порядку.

### Шаг 1 — База данных + Redis
```bash
cd /home/daniil/NetCert
docker compose -f infra/docker-compose.yml up -d postgres redis
# Подожди 5-10 секунд
```

### Шаг 2 — Миграции БД
```bash
cd /home/daniil/NetCert
psql -h localhost -U netcert -d netcert -f backend/migrations/001_initial_schema.sql
psql -h localhost -U netcert -d netcert -f backend/migrations/002_seed_data.sql
# Пароль: netcert
```

### Шаг 3 — Бэкенд (Go)
```bash
cd /home/daniil/NetCert/backend
cp .env.example .env   # только при первом запуске
go run ./cmd/server/
# → http://localhost:8080
```

### Шаг 4 — Фронтенд (Next.js)
```bash
cd /home/daniil/NetCert/frontend
npm install   # только при первом запуске
npm run dev
# → http://localhost:3000
```

---

## 🌐 Что открывать в браузере

| Адрес | Описание |
|-------|----------|
| `http://localhost:3000` | Главная (Landing) |
| `http://localhost:3000/auth/register` | Регистрация |
| `http://localhost:3000/auth/login` | Вход |
| `http://localhost:3000/dashboard` | Дашборд (после входа) |
| `http://localhost:3000/exams` | Список экзаменов |
| `http://localhost:3000/exam/:id` | Прохождение экзамена |
| `http://localhost:8080/health` | Health check API |

---

## ⚡ Через Makefile (если всё установлено)

```bash
make dev-infra     # Docker: postgres + redis
make dev-backend   # Go сервер на :8080
make dev-frontend  # Next.js на :3000
make migrate-up    # Применить миграции
```

---

## 🏗 Архитектура

```
netcert/
├── backend/                    # Go-бэкенд (Clean Architecture)
│   ├── cmd/server/main.go      # Точка входа
│   ├── internal/
│   │   ├── config/             # Конфигурация
│   │   ├── domain/             # Доменные сущности
│   │   ├── repository/postgres/ # Репозитории (PostgreSQL)
│   │   ├── usecase/            # Бизнес-логика
│   │   ├── delivery/http/      # HTTP handlers (Chi)
│   │   ├── middleware/         # Auth middleware (JWT)
│   │   └── pkg/                # Утилиты (JWT, хэширование)
│   ├── migrations/             # SQL миграции + сиды
│   └── go.mod
├── frontend/                   # Next.js 16 фронтенд
│   ├── app/                    # App Router страницы
│   │   ├── auth/               # Login / Register
│   │   ├── dashboard/          # Дашборд пользователя
│   │   ├── exams/              # Список экзаменов
│   │   ├── exam/[id]/          # Прохождение экзамена
│   │   ├── review/[id]/        # Разбор результатов
│   │   └── settings/           # Настройки
│   ├── components/             # UI компоненты (shadcn-стиль)
│   └── lib/                    # API клиент, контекст, утилиты
└── infra/                      # Docker-инфраструктура
    ├── docker-compose.yml
    ├── Dockerfile.backend
    └── Dockerfile.frontend
```

## 🛠 Стек технологий

### Бэкенд
- **Go 1.22+** — чистый язык, высокая производительность
- **Chi** — легковесный HTTP-роутер
- **pgx** — драйвер PostgreSQL
- **JWT** — аутентификация (access + refresh токены)
- **Clean Architecture** — domain → usecase → repository → delivery

### Фронтенд
- **Next.js 16** — React-фреймворк с App Router
- **React 19** + **TypeScript**
- **Tailwind CSS 4** — утилитарный CSS
- **shadcn/ui** — компоненты в bento-grid стиле
- **Framer Motion** — анимации
- **Recharts** — графики и аналитика

### Инфраструктура
- **PostgreSQL 16** — основная БД
- **Redis 7** — кэш и сессии
- **Docker Compose** — локальная разработка

## 📚 Контент (в seed-данных)

**JNCIA-Junos (JN0-101)** — 10 вопросов:
Junos OS Architecture, CLI, OSPF, BGP, Firewall Filters, Static Routing, Interface Types, Configuration Management

**JNCIA-SP (JN0-201)** — 3 вопроса:
MPLS Fundamentals, Architecture, LDP

**CCNA (200-301)** — 3 вопроса:
OSPF AD, VLAN Ranges, RIP

## 🔌 API Endpoints

| Метод | Путь | Описание |
|-------|------|----------|
| GET | `/health` | Health check |
| POST | `/api/v1/auth/register` | Регистрация |
| POST | `/api/v1/auth/login` | Вход |
| GET | `/api/v1/users/me` | Профиль (auth) |
| GET | `/api/v1/tracks` | Список треков |
| GET | `/api/v1/tracks/{slug}` | Детали трека |
| GET | `/api/v1/tracks/{slug}/exams` | Экзамены трека |
| GET | `/api/v1/exams/{examId}` | Детали экзамена |
| POST | `/api/v1/attempts` | Начать попытку (auth) |
| GET | `/api/v1/attempts/{attemptId}` | Получить попытку (auth) |
| POST | `/api/v1/attempts/{attemptId}/answers` | Отправить ответ (auth) |
| POST | `/api/v1/attempts/{attemptId}/complete` | Завершить попытку (auth) |
| GET | `/api/v1/attempts/history` | История попыток (auth) |

## 📋 Планы развития

- [ ] 16 полноценных экзаменов (JNCIA→JNCIE, CCNA→CCIE)
- [ ] JNCIE Lab Engine (Containerlab)
- [ ] Spaced Repetition (SM-2 алгоритм)
- [ ] Аналитика: heatmap, radar chart, predictive readiness
- [ ] Gamification: streak, XP, achievements
- [ ] i18n (RU/EN)
- [ ] OAuth2 (Google/GitHub)
- [ ] PWA / офлайн-режим
