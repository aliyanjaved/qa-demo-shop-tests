import pytest
from playwright.sync_api import Page, expect

from tests.conftest import VALID_USER
from tests.ui.pages import CheckoutPage, LoginPage, ProductsPage, dt

pytestmark = pytest.mark.ui


@pytest.fixture
def shop(page: Page, base_url):
    """Logged-in user on the products page."""
    login = LoginPage(page, base_url)
    login.open()
    login.login(**VALID_USER)
    return ProductsPage(page)


@pytest.mark.smoke
def test_adding_a_product_updates_the_cart_counter(shop):
    assert shop.cart_count() == "0"
    shop.add(1)
    assert shop.cart_count() == "1"


def test_search_filters_the_product_list(shop):
    shop.search("Hat")
    assert shop.names() == ["Sun Hat"]


def test_search_is_case_insensitive(shop):
    # Catches BUG-001 when the app runs with SEEDED_BUGS=true
    shop.search("sun hat")
    assert shop.names() == ["Sun Hat"]


def test_search_without_match_shows_empty_state(shop, page: Page):
    shop.search("zzzz")
    expect(dt(page, "no-results")).to_be_visible()


def test_cart_total_reflects_quantity(shop, page: Page):
    # Catches BUG-002 when the app runs with SEEDED_BUGS=true
    shop.add(2)
    shop.add(2)
    shop.add(2)  # 3 x 9.99
    dt(page, "nav-cart").click()
    expect(dt(page, "qty-2")).to_have_text("3")
    expect(dt(page, "cart-total")).to_have_text("29.97")


def test_removing_an_item_empties_the_cart(shop, page: Page):
    shop.add(1)
    dt(page, "nav-cart").click()
    dt(page, "remove-1").click()
    expect(dt(page, "cart-empty")).to_be_visible()


def test_checkout_requires_address(shop, page: Page):
    # Catches BUG-003 when the app runs with SEEDED_BUGS=true
    shop.add(1)
    dt(page, "nav-cart").click()
    dt(page, "checkout-link").click()
    CheckoutPage(page).fill_and_submit("Ali", "")
    expect(dt(page, "checkout-error")).to_have_text("Name and address are required")


@pytest.mark.smoke
def test_complete_purchase_flow(shop, page: Page):
    shop.add(1)
    shop.add(6)
    dt(page, "nav-cart").click()
    expect(dt(page, "cart-total")).to_have_text("44.99")
    dt(page, "checkout-link").click()
    CheckoutPage(page).fill_and_submit("Ali", "Main St 1")
    expect(dt(page, "order-confirmation")).to_contain_text("Thank you")
