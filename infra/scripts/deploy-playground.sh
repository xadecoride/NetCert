#!/bin/sh
# deploy-playground.sh — Deploy NetCert JunOS Playground topology
# Runs inside the clab-dind container.
# Deploys a single cRPD node for interactive JunOS CLI practice.

set -e

CLAB_DIR="${CLAB_DIR:-/labs/playground}"
TOPOLOGY="${CLAB_DIR}/clab.yml"
CONTAINERLAB="${CONTAINERLAB:-containerlab}"

# Check if cRPD image is available
if docker images --format '{{.Repository}}:{{.Tag}}' | grep -q 'crpd:'; then
    echo "[playground] cRPD image found. Deploying JunOS playground..."
    if ${CONTAINERLAB} inspect -t "${TOPOLOGY}" >/dev/null 2>&1; then
        echo "[playground] Topology already deployed, skipping."
    else
        ${CONTAINERLAB} deploy -t "${TOPOLOGY}"
        echo "[playground] JunOS playground deployed successfully."
        echo "[playground] Connect via: docker exec -it clab-playground-r1 cli"
    fi
else
    echo "[playground] No cRPD image found. Skipping JunOS playground deploy."
    echo "[playground] To enable JunOS CLI lab, download crpd:24.2R1 from Juniper Support Portal."
    echo "[playground]   docker pull crpd:24.2R1"
    echo "[playground] Or load from file:"
    echo "[playground]   docker load -i crpd-24.2R1.tgz"
    echo "[playground] Then restart: docker compose restart backend sandbox"
fi

# Deploy playground — done
echo "[playground] Playground ready."
