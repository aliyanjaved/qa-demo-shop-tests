import pytest
import requests

from tests.conftest import BASE_URL

pytestmark = pytest.mark.api


def add_to_cart(headers, product_id, quantity=1):
    return requests.post(f"{BASE_URL}/api/cart", headers=headers,
                         json={"product_id": product_id, "quantity": quantity}, timeout=5)


def test_cart_requires_authentication():
    assert requests.get(f"{BASE_URL}/api/cart", timeout=5).status_code == 401


@pytest.mark.smoke
def test_add_item_to_cart(auth_headers):
    r = add_to_cart(auth_headers, 1)
    assert r.status_code == 201
    assert r.json()["items"][0]["name"] == "Backpack"


def test_cart_total_takes_quantity_into_account(auth_headers):
    # Catches BUG-002 when the app runs with SEEDED_BUGS=true
    add_to_cart(auth_headers, 2, quantity=3)  # Bike Light 9.99 x 3
    r = requests.get(f"{BASE_URL}/api/cart", headers=auth_headers, timeout=5)
    assert r.json()["total"] == pytest.approx(29.97)


def test_cart_total_sums_multiple_products(auth_headers):
    add_to_cart(auth_headers, 1)  # 29.99
    add_to_cart(auth_headers, 6)  # 15.00
    r = requests.get(f"{BASE_URL}/api/cart", headers=auth_headers, timeout=5)
    assert r.json()["total"] == pytest.approx(44.99)


@pytest.mark.parametrize("quantity", [0, -1, "two"])
def test_invalid_quantity_is_rejected(auth_headers, quantity):
    assert add_to_cart(auth_headers, 1, quantity).status_code == 400


def test_quantity_above_stock_returns_409(auth_headers):
    assert add_to_cart(auth_headers, 4, quantity=6).status_code == 409  # stock is 5


def test_adding_unknown_product_returns_404(auth_headers):
    assert add_to_cart(auth_headers, 9999).status_code == 404


def test_checkout_with_empty_cart_is_rejected(auth_headers):
    r = requests.post(f"{BASE_URL}/api/checkout", headers=auth_headers,
                      json={"name": "Ali", "address": "Main St 1"}, timeout=5)
    assert r.status_code == 400


def test_checkout_requires_address(auth_headers):
    # Catches BUG-003 when the app runs with SEEDED_BUGS=true
    add_to_cart(auth_headers, 1)
    r = requests.post(f"{BASE_URL}/api/checkout", headers=auth_headers,
                      json={"name": "Ali", "address": ""}, timeout=5)
    assert r.status_code == 400


@pytest.mark.smoke
def test_successful_checkout_creates_order_and_empties_cart(auth_headers):
    add_to_cart(auth_headers, 1, quantity=2)
    r = requests.post(f"{BASE_URL}/api/checkout", headers=auth_headers,
                      json={"name": "Ali", "address": "Main St 1"}, timeout=5)
    assert r.status_code == 201
    assert r.json()["order_id"] >= 1001
    cart = requests.get(f"{BASE_URL}/api/cart", headers=auth_headers, timeout=5).json()
    assert cart["items"] == []
