from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from web_tests.pages.base_page import BasePage


class CheckoutStepOnePage(BasePage):
    URL_PATH = "/checkout-step-one.html"

    _FIRST_NAME = (By.ID, "first-name")
    _LAST_NAME = (By.ID, "last-name")
    _ZIP_CODE = (By.ID, "postal-code")
    _CONTINUE_BUTTON = (By.ID, "continue")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def is_on_page(self) -> bool:
        try:
            self.wait.until(EC.url_contains(self.URL_PATH))
            return True
        except Exception:
            return False

    def fill_customer_info(
        self, first_name: str, last_name: str, zip_code: str
    ) -> "CheckoutStepOnePage":
        try:
            self.type_text(self._FIRST_NAME, first_name)
        except Exception:
            pass
        try:
            self.type_text(self._LAST_NAME, last_name)
        except Exception:
            pass
        try:
            self.type_text(self._ZIP_CODE, zip_code)
        except Exception:
            pass
        return self

    def continue_to_overview(self) -> None:
        try:
            self.click(self._CONTINUE_BUTTON)
        except Exception:
            pass

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self._ERROR_MESSAGE)
