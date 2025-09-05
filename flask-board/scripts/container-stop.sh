#!/bin/zsh
set -e
DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$DIR"

echo "Stopping stack via docker compose..."
docker compose down
