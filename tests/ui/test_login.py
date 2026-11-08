import pytest
from playwright.sync_api import Page, expect

from tests.conftest import LOCKED_USER, VALID_USER
from tests.ui.pages import LoginPage, dt

pytestmark = pytest.mark.ui


@pytest.mark.smoke
def test_valid_user_lands_on_products_page(page: Page, base_url):
    login = LoginPage(page, base_url)
    login.open()
    login.login(**VALID_USER)
    expect(page).to_have_url(f"{base_url}/products")
    expect(page.get_by_role("heading", name="Products")).to_be_visible()


def test_wrong_password_shows_error(page: Page, base_url):
    login = LoginPage(page, base_url)
    login.open()
    login.login("standard_user", "wrong")
    expect(dt(page, "login-error")).to_have_text("Invalid credentials")


def test_locked_user_sees_lockout_message(page: Page, base_url):
    login = LoginPage(page, base_url)
    login.open()
    login.login(**LOCKED_USER)
    expect(dt(page, "login-error")).to_have_text("This user is locked out")


def test_empty_form_shows_required_message(page: Page, base_url):
    login = LoginPage(page, base_url)
    login.open()
    dt(page, "login-button").click()
    expect(dt(page, "login-error")).to_contain_text("required")


def test_products_page_redirects_to_login_when_logged_out(page: Page, base_url):
    page.goto(f"{base_url}/products")
    expect(page).to_have_url(f"{base_url}/login")
