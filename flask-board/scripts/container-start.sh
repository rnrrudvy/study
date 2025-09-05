#!/bin/zsh
set -e
DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$DIR"

# Allow overriding host port used in compose via env substitution if defined in compose
HOST_PORT="${1:-5001}"
export HOST_PORT

# Optional build: BUILD=1 ./scripts/container-start.sh
if [ -n "${BUILD:-}" ]; then
  echo "Building images via docker compose..."
  docker compose build
fi

echo "Starting stack via docker compose (HOST_PORT=${HOST_PORT})..."
docker compose up -d

echo "Open: http://127.0.0.1:${HOST_PORT}"
