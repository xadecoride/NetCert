#!/bin/sh
set -eu

# ============================================================
# NetCert — DinD Entrypoint Wrapper
# ============================================================
# Запускает Docker daemon через штатный dockerd-entrypoint.sh,
# дожидается готовности dockerd, затем автоматически деплоит
# playground топологию (cRPD) если образ доступен.
#
# Сохраняет оригинальное поведение dockerd-entrypoint.sh
# (TLS, iptables, rootless mode) — работает в background.
# ============================================================

# ── 1. Запуск Docker daemon ────────────────────────────────
echo "[dind] Starting Docker daemon via dockerd-entrypoint.sh..."
/usr/local/bin/dockerd-entrypoint.sh &
DOCKER_PID=$!

# ── 2. Ожидание готовности dockerd ─────────────────────────
echo "[dind] Waiting for Docker daemon to be ready..."
for i in $(seq 1 90); do
    if docker info >/dev/null 2>&1; then
        echo "[dind] Docker daemon ready (attempt $i)."
        break
    fi
    if ! kill -0 "$DOCKER_PID" 2>/dev/null; then
        echo "[dind] ERROR: Docker daemon process exited prematurely."
        wait "$DOCKER_PID" || true
        exit 1
    fi
    sleep 1
done

if ! docker info >/dev/null 2>&1; then
    echo "[dind] ERROR: Docker daemon did not become ready within 90 seconds."
    exit 1
fi

# ── 3. Деплой playground топологии ─────────────────────────
echo "[dind] Checking for cRPD image to deploy playground topology..."

if docker images --format '{{.Repository}}:{{.Tag}}' | grep -q 'crpd:'; then
    echo "[dind] cRPD image found. Deploying JunOS playground..."
    if docker ps --format '{{.Names}}' | grep -q 'clab-netcert-playground'; then
        echo "[dind] Playground topology already deployed, skipping."
    else
        if containerlab deploy -t /labs/playground/clab.yml; then
            echo "[dind] Playground deployed successfully."
            echo "[dind] Connect via: docker exec -it clab-playground-r1 cli"
        else
            echo "[dind] WARNING: Playground deploy failed. Check containerlab logs."
        fi
    fi
else
    echo "[dind] No cRPD image found. Skipping playground deploy."
    echo "[dind] To enable JunOS CLI playground, pull crpd:24.2R1:"
    echo "[dind]   docker exec netcert-staging-clab-dind docker pull crpd:24.2R1"
    echo "[dind] Then restart clab-dind to auto-deploy."
fi

# ── 4. Мониторинг Docker daemon ────────────────────────────
echo "[dind] Init complete. Monitoring Docker daemon (PID: $DOCKER_PID)..."
wait "$DOCKER_PID"
