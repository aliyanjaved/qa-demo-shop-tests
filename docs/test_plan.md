# Test Plan: Demo Web Shop

## 1. Objective
Verify that the core shopping flows (login, product search, cart, checkout) of the demo web shop
work correctly through both the REST API and the browser UI, and make regressions visible in CI.

## 2. Scope
| In scope | Out of scope |
|---|---|
| Authentication (valid, invalid, locked, missing fields) | Performance and load testing |
| Product listing, lookup, search | Security testing beyond basic auth checks |
| Cart: add, remove, quantity, stock limit, total | Payment providers (not implemented) |
| Checkout: validation, order creation, cart cleanup | Cross-browser testing (Chromium only) |

## 3. Test approach
- **API tests** (pytest + requests): fast, cover status codes, validation rules, business logic and error handling.
- **UI tests** (Playwright + pytest, page-object pattern): cover user-visible behaviour and critical flows end to end.
- **Smoke subset** (`-m smoke`): 7 critical-path tests for a quick check on every commit.
- **Test data / isolation:** every test resets server state through `POST /api/test/reset`; each UI test uses a fresh browser context.
- **Locators:** stable `data-test` attributes instead of CSS/text where possible.

## 4. Environments
Local (Python venv), Docker Compose, GitHub Actions, Jenkins (see `Jenkinsfile`).

## 5. Entry / exit criteria
- Entry: app starts and `/health` returns 200.
- Exit: all tests pass on the clean build; no open defect of severity High or above.

## 6. Risks
- UI tests depend on markup (mitigated with `data-test` attributes and page objects).
- In-memory state in the demo app means tests must not run in parallel against one server instance.

## 7. Defect handling
Defects are documented in `docs/defect_reports.md` with steps to reproduce, expected/actual result,
severity and the automated test that detects them. The app can be started with `SEEDED_BUGS=true`
to reproduce them.
