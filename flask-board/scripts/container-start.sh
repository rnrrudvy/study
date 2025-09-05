#!/bin/zsh
set -e
IMAGE="flask-board:local"
NAME="flask-board"
HOST_PORT="${1:-5001}"
CONTAINER_PORT="${2:-5000}"

# Build if image missing
if ! docker image inspect "$IMAGE" >/dev/null 2>&1; then
  echo "Image $IMAGE not found. Building..."
  docker build -t "$IMAGE" .
fi

# Stop existing container with same name
if docker ps -a --format '{{.Names}}' | grep -q "^${NAME}$"; then
  echo "Stopping existing container ${NAME}..."
  docker stop "$NAME" >/dev/null || true
fi

# Run
echo "Starting container ${NAME} on port ${HOST_PORT} -> ${CONTAINER_PORT}"
docker run -d --name "$NAME" -p ${HOST_PORT}:${CONTAINER_PORT} --rm "$IMAGE"

echo "Open: http://127.0.0.1:${HOST_PORT}"
