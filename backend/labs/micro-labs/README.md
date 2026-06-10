# NetCert Pro — Concept Micro-Labs (Level L1)

Пять стартовых микро-лаб по фундаментальным сетевым технологиям Juniper JunOS.

## Структура

```
micro-labs/
├── README.md                          # ← этот файл
├── 01-junos-cli-basics/              # JunOS CLI basics (2 cRPD)
├── 02-ospf-adjacency/                # OSPF adjacency (3 cRPD triangle)
├── 03-ebgp-peering/                  # EBGP peering (3 cRPD line)
├── 04-isis-single-level/             # IS-IS single-level (3 cRPD triangle)
└── 05-mpls-lsp/                      # MPLS LSP с LDP (3 cRPD line)
```

Каждая микро-лаба содержит:

| Файл | Назначение |
|------|-----------|
| `clab.yml` | Containerlab топология (kind: juniper_crpd) |
| `configs/*.cfg` | Начальные конфиги для каждой ноды |
| `task.md` | Описание задачи, hints, критерии успеха |
| `grade.py` | Auto-grading скрипт (partial scoring) |

## Требования

- [Containerlab](https://containerlab.dev/install/) v0.55+
- [cRPD образ](https://hub.docker.com/r/juniper/crpd) (`docker pull juniper/crpd`)
- Python 3.10+ с `scrapli` (рекомендуется) или `paramiko` (fallback)

## Быстрый старт

```bash
# 1. Развернуть топологию
cd micro-labs/01-junos-cli-basics
sudo clab deploy --reconfigure -t clab.yml

# 2. Подключиться к устройству
ssh admin@clab-junos-cli-basics-r1

# 3. Выполнить задания из task.md

# 4. Запустить проверку
python3 grade.py --r1-ip $(sudo docker inspect clab-junos-cli-basics-r1 -f '{{.NetworkSettings.IPAddress}}') \
                 --r2-ip $(sudo docker inspect clab-junos-cli-basics-r2 -f '{{.NetworkSettings.IPAddress}}')

# 5. Удалить топологию
sudo clab destroy -t clab.yml
```

## Сводка лаб

| # | Технология | Ноды | Время | Уровень | Темы |
|---|-----------|------|-------|---------|------|
| 01 | JunOS CLI Basics | 2 cRPD | 15 мин | JNCIA | show, configure, commit, interfaces |
| 02 | OSPF Adjacency | 3 cRPD (triangle) | 20 мин | JNCIA/JNCIS | area 0, passive, adjacency check |
| 03 | EBGP Peering | 3 cRPD (line) | 25 мин | JNCIS/JNCIP | EBGP multihop, AS-path, next-hop |
| 04 | IS-IS Single-Level | 3 cRPD (triangle) | 20 мин | JNCIS/JNCIP | NET, ISO, Level 1 adjacencies |
| 05 | MPLS LSP | 3 cRPD (line) | 30 мин | JNCIS/JNCIP | OSPF + LDP + RSVP, LSP status |

## Progressive Disclosure

Каждая лаба построена по принципу **Progressive Disclosure**:

1. **Task 0 (Pre-lab):** Проверить connectivity, базовые show-команды
2. **Task 1 (Config):** Базовая настройка протокола
3. **Task 2 (Verify):** Проверка adjacencies/sessions
4. **Task 3 (Advanced):** Дополнительная конфигурация / оптимизация
5. **Task 4 (Troubleshoot):** Внесённая неисправность, которую нужно найти и исправить

## Grading

```bash
# JSON output (для интеграции с API)
python3 grade.py --r1-ip 172.31.0.2 --r2-ip 172.31.0.3 --r3-ip 172.31.0.4 --output json

# Human-readable output
python3 grade.py --r1-ip 172.31.0.2 --r2-ip 172.31.0.3 --r3-ip 172.31.0.4
```

Все скрипты используют **partial scoring** (не all-or-nothing) через 5 критериев по 15-25 баллов. Порог прохождения — 70%.

## Docker Compose / API Integration

Микро-лабы интегрируются в платформу через:

1. **SQL Migration** `042_micro_labs.sql` — создаёт таблицу `micro_labs` + `chapter_micro_labs` + seed data
2. **Go Orchestrator** — запускает `clab deploy` по запросу пользователя, выделяет порты, возвращает URL xterm.js
3. **WebSocket** — стримит вывод grade.py в реальном времени
