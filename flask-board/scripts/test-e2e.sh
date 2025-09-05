#!/bin/zsh
set -e
DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$DIR"

# Ensure dev deps
python3 -m venv .venv >/dev/null 2>&1 || true
source .venv/bin/activate
python -m pip install --upgrade pip >/dev/null 2>&1
pip install -r requirements-dev.txt >/dev/null 2>&1

export BASE_URL="${BASE_URL:-http://127.0.0.1:5001}"
mkdir -p result
echo "Running E2E tests against ${BASE_URL}"
pytest -q tests/test_e2e.py --junitxml=result/junit.xml --html=result/report.html --self-contained-html
STATUS=$?
if [ $STATUS -eq 0 ]; then
  echo "E2E PASSED" | tee result/summary.txt
else
  echo "E2E FAILED (code=$STATUS)" | tee result/summary.txt
fi
exit $STATUS

