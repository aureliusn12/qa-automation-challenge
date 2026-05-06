from selenium.webdriver.common.by import By

from web_tests.pages.base_page import BasePage


class CartPage(BasePage):
    URL_PATH = "/cart.html"

    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_NAMES = (By.CLASS_NAME, "inventory_item_name")
    _CHECKOUT_BUTTON = (By.ID, "checkout")
    _CONTINUE_SHOPPING = (By.ID, "continue-shopping")

    def is_on_page(self) -> bool:
        return self.URL_PATH in self.current_url()

    def get_item_count(self) -> int:
        return len(self.find_all(self._CART_ITEMS))

    def get_item_names(self) -> list:
        return [el.text for el in self.find_all(self._ITEM_NAMES)]

    def proceed_to_checkout(self) -> None:
        self.click(self._CHECKOUT_BUTTON)

    def continue_shopping(self) -> None:
        self.click(self._CONTINUE_SHOPPING)
