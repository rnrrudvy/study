#!/bin/zsh
set -e
DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$DIR"

if [ -f .flask.pid ]; then
  PID=$(cat .flask.pid)
  if kill "$PID" 2>/dev/null; then
    echo "Stopped local Flask (PID: $PID)"
    rm -f .flask.pid
    exit 0
  else
    echo "PID $PID not running. Cleaning pid file and falling back to port scan."
    rm -f .flask.pid
  fi
fi

PIDS=$(lsof -ti :5000 2>/dev/null)
if [ -z "$PIDS" ]; then
  echo "No local Flask found on port 5000."
  exit 0
fi
print -l $PIDS | xargs kill
print -l $PIDS | tr '\n' ' ' | sed 's/ $/\n/' | sed 's/^/Stopped processes: /'
