import pytest
import requests

from tests.conftest import BASE_URL, LOCKED_USER, VALID_USER

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_login_with_valid_credentials_returns_token():
    r = requests.post(f"{BASE_URL}/api/login", json=VALID_USER, timeout=5)
    assert r.status_code == 200
    assert r.json()["token"]


def test_login_with_wrong_password_is_rejected():
    r = requests.post(f"{BASE_URL}/api/login",
                      json={"username": "standard_user", "password": "wrong"}, timeout=5)
    assert r.status_code == 401
    assert r.json()["error"] == "invalid credentials"


def test_login_for_locked_user_returns_423():
    r = requests.post(f"{BASE_URL}/api/login", json=LOCKED_USER, timeout=5)
    assert r.status_code == 423


@pytest.mark.parametrize("payload", [{}, {"username": "standard_user"}, {"password": "secret123"}])
def test_login_with_missing_fields_returns_400(payload):
    r = requests.post(f"{BASE_URL}/api/login", json=payload, timeout=5)
    assert r.status_code == 400
