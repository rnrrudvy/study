#!/bin/zsh
set -e
DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$DIR"

# Create venv if missing
if [ ! -d ".venv" ]; then
  # uv venv needs to be run from a project root with pyproject.toml or git repo
  # to auto-detect the project name. Since we are in a git repo, this is fine.
  uv venv
fi
source .venv/bin/activate
uv pip install -r requirements.txt >/dev/null 2>&1

# Kill anything on port 5000 to avoid conflicts
(lsof -ti :5000 | xargs kill) >/dev/null 2>&1 || true

nohup python app.py > /tmp/flask-board-local.out 2>&1 &
PID=$!
echo $PID > .flask.pid

echo "Started local Flask (PID: $PID) on http://127.0.0.1:5000"
echo "Logs: /tmp/flask-board-local.out"
