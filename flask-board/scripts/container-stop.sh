#!/bin/zsh
set -e
NAME="flask-board"
if docker ps --format '{{.Names}}' | grep -q "^${NAME}$"; then
  docker stop "$NAME"
  echo "Stopped container ${NAME}"
else
  echo "No running container named ${NAME}"
fi
