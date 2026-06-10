#!/usr/bin/env bash
# ============================================================
# deploy-labs.sh — NetCert Lab Infrastructure Deploy Script
# ============================================================
# Разворачивает или обновляет лабораторную инфраструктуру
# на staging-сервере с Containerlab Docker-in-Docker.
#
# Использование:
#   ./infra/scripts/deploy-labs.sh              # deploy/update
#   ./infra/scripts/deploy-labs.sh --build       # rebuild & deploy
#   ./infra/scripts/deploy-labs.sh --down        # stop all
#   ./infra/scripts/deploy-labs.sh --logs        # tail logs
#   ./infra/scripts/deploy-labs.sh --seed        # seed lab data
# ============================================================

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
COMPOSE_FILE="${SCRIPT_DIR}/infra/docker-compose.staging.yml"
PROJECT_NAME="netcert-staging"

# Containerlab version to install inside DinD
CLAB_VERSION="v0.75.0"
CLAB_APK_URL="https://github.com/srl-labs/containerlab/releases/download/${CLAB_VERSION}/containerlab_0.75.0_linux_amd64.apk"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

log_info()  { echo -e "${CYAN}[INFO]${NC}  $*"; }
log_ok()    { echo -e "${GREEN}[OK]${NC}    $*"; }
log_warn()  { echo -e "${YELLOW}[WARN]${NC}  $*"; }
log_error() { echo -e "${RED}[ERROR]${NC} $*"; }

check_prerequisites() {
    log_info "Checking prerequisites..."

    if ! command -v docker &>/dev/null; then
        log_error "Docker is not installed. Install Docker first."
        exit 1
    fi

    if ! command -v docker compose &>/dev/null; then
        log_error "Docker Compose v2 is not installed."
        exit 1
    fi

    docker info &>/dev/null || {
        log_error "Docker daemon is not running."
        exit 1
    }

    log_ok "All prerequisites satisfied"
}

deploy() {
    local BUILD_FLAG="${1:-}"

    check_prerequisites

    log_info "Deploying NetCert Lab Infrastructure..."

    # Deploy stack (cRPD image is pulled later in verify_clab)
    if [ "${BUILD_FLAG}" == "--build" ]; then
        log_info "Building and deploying (--build)..."
        docker compose \
            -f "${COMPOSE_FILE}" \
            -p "${PROJECT_NAME}" \
            up -d --build
    else
        log_info "Deploying without rebuild..."
        docker compose \
            -f "${COMPOSE_FILE}" \
            -p "${PROJECT_NAME}" \
            up -d
    fi

    # Wait for services
    log_info "Waiting for services to become healthy..."
    sleep 5

    # Check health
    docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        ps

    log_ok "Lab infrastructure deployed successfully!"
    log_info ""
    log_info "Services:"
    log_info "  Frontend:     http://localhost:3000"
    log_info "  API:          http://localhost:8080"
    log_info "  WebSocket:    ws://localhost:8080/ws/lab/{submissionId}/{deviceName}"
    log_info "  Containerlab: docker exec -it netcert-staging-clab-dind containerlab version"
    log_info ""
    log_info "Useful commands:"
    log_info "  Check logs:   docker compose -f ${COMPOSE_FILE} logs -f"
    log_info "  Stop all:     docker compose -f ${COMPOSE_FILE} down"
    log_info "  Start lab:    curl -X POST http://localhost:8080/api/v1/labs/start"
}

seed_data() {
    log_info "Seeding lab data into database..."

    # Run the 042_micro_labs.sql migration
    docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        exec -T postgres psql -U netcert -d netcert \
        -f /dev/stdin < "${SCRIPT_DIR}/backend/migrations/042_micro_labs.sql" 2>/dev/null || \
    log_warn "Could not seed lab data. Run migrations manually."

    # Run the 050_lab_sessions.sql migration
    docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        exec -T postgres psql -U netcert -d netcert \
        -f /dev/stdin < "${SCRIPT_DIR}/backend/migrations/050_lab_sessions.sql" 2>/dev/null || \
    log_warn "Could not create lab sessions tables."

    log_ok "Lab data seeded successfully!"
}

verify_clab() {
    log_info "Verifying Containerlab setup..."

    # Check if DinD is running
    if ! docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        exec -T clab-dind docker info &>/dev/null; then
        log_error "Containerlab DinD is not running. Deploy first."
        exit 1
    fi

    # Check containerlab version inside DinD
    log_info "Containerlab version:"
    docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        exec -T clab-dind containerlab version 2>/dev/null || \
    log_warn "containerlab not found inside DinD. Installing..."

    # Install containerlab if not found (Alpine DinD — use APK directly)
    docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        exec -T clab-dind sh -c "
            if ! command -v containerlab &>/dev/null; then
                echo 'Installing containerlab via APK...' &&
                apk add --no-cache curl &&
                curl -sL "${CLAB_APK_URL}" -o /tmp/clab.apk &&
                apk add --allow-untrusted /tmp/clab.apk &&
                rm /tmp/clab.apk &&
                apk del curl &&
                echo 'containerlab installed successfully'
            fi
        " 2>/dev/null

    # Attempt to pull cRPD image (non-blocking — will be pulled on first lab start)
    log_info "Checking Juniper cRPD image..."
    docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        exec -T clab-dind sh -c "
            docker images crpd:24.2R1 | grep -q crpd || {
                echo 'cRPD image not found. Pulling...' &&
                docker pull crpd:24.2R1
            }
        " 2>/dev/null || \
    log_warn "cRPD image not available. It will be pulled on first lab start."

    log_ok "Containerlab verification complete!"
}

down() {
    log_info "Stopping lab infrastructure..."
    docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        down --remove-orphans
    log_ok "All services stopped."
}

logs() {
    docker compose \
        -f "${COMPOSE_FILE}" \
        -p "${PROJECT_NAME}" \
        logs -f "${@}"
}

# ─── CLI ────────────────────────────────────────────────────

case "${1:-deploy}" in
    deploy)
        deploy "${2:-}"
        verify_clab
        ;;
    --build)
        deploy "--build"
        verify_clab
        ;;
    --down|down|stop)
        down
        ;;
    --logs|logs)
        shift
        logs "$@"
        ;;
    --seed|seed)
        seed_data
        ;;
    --verify|verify)
        verify_clab
        ;;
    --help|help|-h)
        echo "Usage: $0 [command]"
        echo ""
        echo "Commands:"
        echo "  deploy          Deploy/update lab infrastructure (default)"
        echo "  deploy --build  Rebuild and deploy"
        echo "  down|stop       Stop all services"
        echo "  logs [svc]      Tail logs (optional: filter by service name)"
        echo "  seed            Seed lab data into database"
        echo "  verify          Verify Containerlab setup"
        echo "  help            Show this help"
        ;;
    *)
        log_error "Unknown command: ${1}"
        echo "Usage: $0 [deploy|down|logs|seed|verify|help]"
        exit 1
        ;;
esac
