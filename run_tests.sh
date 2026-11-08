#!/usr/bin/env bash
# Usage: ./run_tests.sh [--bugs] [pytest args...]
#   ./run_tests.sh                 run everything against the clean app
#   ./run_tests.sh --bugs          run against the app with 3 seeded defects
#   ./run_tests.sh -m smoke        run only smoke tests
set -euo pipefail
cd "$(dirname "$0")"

mkdir -p reports
BUGS=false
if [[ "${1:-}" == "--bugs" ]]; then BUGS=true; shift; fi

SEEDED_BUGS=$BUGS python app/app.py > reports/app.log 2>&1 &
APP_PID=$!
trap 'kill $APP_PID 2>/dev/null || true' EXIT

for _ in $(seq 1 20); do
  curl -sf http://localhost:5000/health > /dev/null && break
  sleep 0.5
done

echo "Running tests (SEEDED_BUGS=$BUGS)"
pytest "$@"
