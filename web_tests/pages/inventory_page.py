from selenium.webdriver.common.by import By

from web_tests.pages.base_page import BasePage


class InventoryPage(BasePage):
    URL_PATH = "/inventory.html"

    _PAGE_TITLE = (By.CLASS_NAME, "title")
    _CART_LINK = (By.CLASS_NAME, "shopping_cart_link")
    _CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")

    def _add_button(self, product_name: str) -> tuple:
        slug = product_name.lower().replace(" ", "-")
        return (By.ID, f"add-to-cart-{slug}")

    def _remove_button(self, product_name: str) -> tuple:
        slug = product_name.lower().replace(" ", "-")
        return (By.ID, f"remove-{slug}")

    def is_on_page(self) -> bool:
        return self.URL_PATH in self.current_url()

    def get_title(self) -> str:
        return self.get_text(self._PAGE_TITLE)

    def add_product(self, product_name: str) -> "InventoryPage":
        self.click(self._add_button(product_name))
        return self

    def remove_product(self, product_name: str) -> "InventoryPage":
        self.click(self._remove_button(product_name))
        return self

    def get_cart_count(self) -> int:
        if self.is_visible(self._CART_BADGE):
            return int(self.get_text(self._CART_BADGE))
        return 0

    def go_to_cart(self) -> None:
        self.click(self._CART_LINK)
