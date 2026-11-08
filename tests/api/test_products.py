import pytest
import requests

from tests.conftest import BASE_URL

pytestmark = pytest.mark.api


@pytest.mark.smoke
def test_product_list_is_not_empty_and_has_required_fields():
    r = requests.get(f"{BASE_URL}/api/products", timeout=5)
    assert r.status_code == 200
    products = r.json()["products"]
    assert len(products) > 0
    for p in products:
        assert {"id", "name", "price", "stock"} <= p.keys()
        assert p["price"] > 0


def test_get_product_by_id():
    r = requests.get(f"{BASE_URL}/api/products/1", timeout=5)
    assert r.status_code == 200
    assert r.json()["name"] == "Backpack"


def test_unknown_product_returns_404():
    assert requests.get(f"{BASE_URL}/api/products/9999", timeout=5).status_code == 404


def test_search_returns_only_matching_products():
    r = requests.get(f"{BASE_URL}/api/products", params={"q": "Bottle"}, timeout=5)
    names = [p["name"] for p in r.json()["products"]]
    assert names == ["Water Bottle"]


@pytest.mark.parametrize("query", ["backpack", "BACKPACK", "BackPack"])
def test_search_is_case_insensitive(query):
    # Catches BUG-001 when the app runs with SEEDED_BUGS=true
    r = requests.get(f"{BASE_URL}/api/products", params={"q": query}, timeout=5)
    names = [p["name"] for p in r.json()["products"]]
    assert names == ["Backpack"]
