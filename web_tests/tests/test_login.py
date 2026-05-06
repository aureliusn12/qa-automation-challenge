from web_tests.data.test_data import LOCKED_USER, STANDARD_USER
from web_tests.pages.inventory_page import InventoryPage
from web_tests.pages.login_page import LoginPage


class TestLogin:
    def test_successful_login_lands_on_inventory(self, logged_in_driver):
        assert InventoryPage(logged_in_driver).is_on_page()

    def test_inventory_page_title_is_products(self, logged_in_driver):
        assert InventoryPage(logged_in_driver).get_title() == "Products"

    def test_locked_user_cannot_login(self, driver):
        login = LoginPage(driver)
        login.open().login(LOCKED_USER.username, LOCKED_USER.password)
        assert login.is_error_displayed()

    def test_locked_user_error_contains_locked_out(self, driver):
        login = LoginPage(driver)
        login.open().login(LOCKED_USER.username, LOCKED_USER.password)
        assert "locked out" in login.get_error_message().lower()

    def test_empty_credentials_show_error(self, driver):
        login = LoginPage(driver)
        login.open().click_login()
        assert login.is_error_displayed()

    def test_missing_password_shows_error(self, driver):
        login = LoginPage(driver)
        login.open().enter_username(STANDARD_USER.username).click_login()
        assert login.is_error_displayed()
