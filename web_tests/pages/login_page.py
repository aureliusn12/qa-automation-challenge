from selenium.webdriver.common.by import By

from web_tests.pages.base_page import BasePage


class LoginPage(BasePage):
    URL = "https://www.saucedemo.com/"

    _USERNAME_INPUT = (By.ID, "user-name")
    _PASSWORD_INPUT = (By.ID, "password")
    _LOGIN_BUTTON = (By.ID, "login-button")
    _ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")

    def open(self) -> "LoginPage":
        self.driver.get(self.URL)
        return self

    def enter_username(self, username: str) -> "LoginPage":
        self.type_text(self._USERNAME_INPUT, username)
        return self

    def enter_password(self, password: str) -> "LoginPage":
        self.type_text(self._PASSWORD_INPUT, password)
        return self

    def click_login(self) -> None:
        self.click(self._LOGIN_BUTTON)

    def login(self, username: str, password: str) -> None:
        self.enter_username(username).enter_password(password).click_login()

    def get_error_message(self) -> str:
        return self.get_text(self._ERROR_MESSAGE)

    def is_error_displayed(self) -> bool:
        return self.is_visible(self._ERROR_MESSAGE)
