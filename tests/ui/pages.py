"""Page objects: keep locators in one place so tests stay readable."""
from playwright.sync_api import Page


def dt(page: Page, name: str):
    return page.locator(f'[data-test="{name}"]')


class LoginPage:
    def __init__(self, page: Page, base_url: str):
        self.page, self.base_url = page, base_url

    def open(self):
        self.page.goto(f"{self.base_url}/login")

    def login(self, username: str, password: str):
        dt(self.page, "username").fill(username)
        dt(self.page, "password").fill(password)
        dt(self.page, "login-button").click()


class ProductsPage:
    def __init__(self, page: Page):
        self.page = page

    def search(self, text: str):
        dt(self.page, "search").fill(text)
        dt(self.page, "search-button").click()

    def add(self, product_id: int):
        dt(self.page, f"add-{product_id}").click()

    def names(self):
        return dt(self.page, "product-name").all_inner_texts()

    def cart_count(self) -> str:
        return dt(self.page, "cart-count").inner_text()


class CheckoutPage:
    def __init__(self, page: Page):
        self.page = page

    def fill_and_submit(self, name: str, address: str):
        dt(self.page, "name").fill(name)
        dt(self.page, "address").fill(address)
        dt(self.page, "place-order").click()
