#!/usr/bin/env bash
# ============================================================
# NetCert — чистый подъём стека одной командой.
#
# Гарантирует, что фронтенд стартует на порту 3000,
# а API — на 8080, независимо от старых записей в .env.
#
# Использование:
#   sudo bash scripts/docker-up.sh
# ============================================================
set -euo pipefail

cd "$(dirname "${BASH_SOURCE[0]}")/.."

# Убираем переопределения портов фронтенда/бэкенда из .env,
# чтобы не было подмены 3000 -> 13000 и т.п.
if [[ -f .env ]]; then
  sed -i '/^[[:space:]]*FRONTEND_PORT=/d; /^[[:space:]]*BACKEND_PORT=/d' .env
  echo "==> .env: переопределения FRONTEND_PORT/BACKEND_PORT удалены"
fi

echo "==> Поднимаем стек (docker compose up --build -d)"
docker compose up --build -d

echo
echo "==> Статус сервисов:"
docker compose ps

echo
echo "==> Публикуемые порты:"
docker compose ps --format 'table {{.Name}}\t{{.Ports}}'

echo
echo "==> Сайт:      http://localhost:3000"
echo "==> API health: http://localhost:8080/health"
