#!/bin/zsh
set -e
DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$DIR"

# Create venv if missing
if [ ! -d ".venv" ]; then
  python3 -m venv .venv
fi
source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements.txt >/dev/null 2>&1

# Kill anything on port 5000 to avoid conflicts
(lsof -ti :5000 | xargs kill) >/dev/null 2>&1 || true

nohup python app.py > /tmp/flask-board-local.out 2>&1 &
PID=$!
echo $PID > .flask.pid

echo "Started local Flask (PID: $PID) on http://127.0.0.1:5000"
echo "Logs: /tmp/flask-board-local.out"
