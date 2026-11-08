# QA Demo Shop: Test Automation Suite

Automated API and UI tests for a small demo web shop (login, product search, cart, checkout),
with Docker, CI pipelines, and documented test plan, test cases and defect reports.

**Tech:** Python, Pytest, Playwright, Requests, Postman, Docker / Docker Compose, Jenkins (Jenkinsfile),
GitHub Actions, Git, Bash.

> The shop in `app/` is a deliberately small system under test. The focus of this project is the
> test design and automation in `tests/`, the pipelines, and the documentation in `docs/`.

## What is covered
- **API tests:** authentication, product search, cart rules (quantity, stock, totals), checkout validation.
- **UI tests (Playwright, page-object pattern):** login, search, cart, full purchase flow.
- **Smoke subset** (`-m smoke`) for quick checks, plus HTML and JUnit reports.
- **Seeded defects:** start the app with `SEEDED_BUGS=true` and 8 tests fail, pointing to 3 documented bugs.

## Run locally
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
playwright install chromium

./run_tests.sh              # all tests against the clean app (38 pass)
./run_tests.sh --bugs       # against the app with 3 seeded defects (8 fail)
./run_tests.sh -m smoke     # smoke tests only
```
Reports are written to `reports/report.html` and `reports/junit.xml`.

## Run with Docker
```bash
docker compose --profile test run --rm tests            # clean app
SEEDED_BUGS=true docker compose --profile test run --rm tests   # seeded defects
docker compose down -v
```

## CI
- `.github/workflows/ci.yml`: runs the suite on every push (second job demonstrates the seeded defects and is allowed to fail).
- `Jenkinsfile`: builds the images, runs the suite in Docker, publishes JUnit results and reports.

## Postman
Import `postman/demo-shop.postman_collection.json`, start the app, and run the collection
(three requests check the seeded defects).

## Structure
```
app/        demo shop (Flask) with REST API and UI
tests/api/  API tests            tests/ui/  UI tests + page objects
docs/       test plan, test cases, defect reports
postman/    Postman collection   Jenkinsfile, .github/workflows/ci.yml, docker-compose.yml
```
