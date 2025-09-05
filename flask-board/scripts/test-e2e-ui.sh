#!/bin/zsh
set -e
DIR="$(cd "$(dirname "$0")"/.. && pwd)"
cd "$DIR"

# Install Node deps locally (no global install)
if [ ! -d node_modules ]; then
  npm install --silent
fi

# Ensure browsers installed
npx --yes playwright install chromium --with-deps 1>/dev/null

export BASE_URL="${BASE_URL:-http://127.0.0.1:5001}"
mkdir -p result
echo "Running UI E2E against ${BASE_URL}"
# Ensure server reflects latest templates
BUILD=1 ./scripts/container-start.sh >/dev/null 2>&1 || true
npx --yes playwright test || true

# Summarize result path
echo "UI report: result/ui-report/index.html" | tee -a result/summary.txt
echo "UI artifacts (video/trace): result/ui-artifacts" | tee -a result/summary.txt

