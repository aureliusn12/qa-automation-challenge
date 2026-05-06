from selenium.webdriver.common.by import By

from web_tests.pages.base_page import BasePage


class CheckoutCompletePage(BasePage):
    URL_PATH = "/checkout-complete.html"
    EXPECTED_HEADER = "Thank you for your order!"

    _COMPLETE_HEADER = (By.CLASS_NAME, "complete-header")
    _COMPLETE_TEXT = (By.CLASS_NAME, "complete-text")
    _BACK_HOME_BUTTON = (By.ID, "back-to-products")

    def is_on_page(self) -> bool:
        return self.URL_PATH in self.current_url()

    def get_confirmation_header(self) -> str:
        return self.get_text(self._COMPLETE_HEADER)

    def get_confirmation_text(self) -> str:
        return self.get_text(self._COMPLETE_TEXT)

    def is_order_confirmed(self) -> bool:
        return self.get_confirmation_header() == self.EXPECTED_HEADER

    def go_back_home(self) -> None:
        self.click(self._BACK_HOME_BUTTON)
