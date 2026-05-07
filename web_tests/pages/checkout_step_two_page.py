from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from web_tests.pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    URL_PATH = "/checkout-step-two.html"

    _CART_ITEMS = (By.CLASS_NAME, "cart_item")
    _ITEM_TOTAL = (By.CLASS_NAME, "summary_subtotal_label")
    _TOTAL = (By.CLASS_NAME, "summary_total_label")
    _FINISH_BUTTON = (By.ID, "finish")
    _CANCEL_BUTTON = (By.ID, "cancel")

    def is_on_page(self) -> bool:
        try:
            self.wait.until(EC.url_contains(self.URL_PATH))
            return True
        except Exception:
            return False

    def get_item_count(self) -> int:
        return len(self.find_all(self._CART_ITEMS))

    def get_item_total_text(self) -> str:
        return self.get_text(self._ITEM_TOTAL)

    def get_total_text(self) -> str:
        return self.get_text(self._TOTAL)

    def finish_purchase(self) -> None:
        self.click(self._FINISH_BUTTON)
        self.wait.until(EC.url_contains("/checkout-complete.html"))

    def cancel(self) -> None:
        self.click(self._CANCEL_BUTTON)
