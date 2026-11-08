import os

import pytest
import requests

BASE_URL = os.getenv("BASE_URL", "http://localhost:5000")
VALID_USER = {"username": "standard_user", "password": "secret123"}
LOCKED_USER = {"username": "locked_user", "password": "secret123"}


@pytest.fixture(scope="session")
def base_url():
    """Overrides the pytest-base-url fixture so UI and API tests share one URL."""
    return BASE_URL


@pytest.fixture(autouse=True)
def reset_state():
    """Every test starts from a clean server state (tokens, carts, orders)."""
    requests.post(f"{BASE_URL}/api/test/reset", timeout=5)


@pytest.fixture
def auth_headers():
    resp = requests.post(f"{BASE_URL}/api/login", json=VALID_USER, timeout=5)
    assert resp.status_code == 200, "precondition failed: login must work"
    return {"Authorization": f"Bearer {resp.json()['token']}"}
