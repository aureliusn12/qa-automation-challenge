import pytest

from web_tests.pages.cart_page import CartPage
from web_tests.pages.checkout_complete_page import CheckoutCompletePage
from web_tests.pages.checkout_step_one_page import CheckoutStepOnePage
from web_tests.pages.checkout_step_two_page import CheckoutStepTwoPage
from web_tests.pages.inventory_page import InventoryPage
from web_tests.pages.login_page import LoginPage


@pytest.fixture
def login_page(driver) -> LoginPage:
    return LoginPage(driver)


@pytest.fixture
def inventory_page(driver) -> InventoryPage:
    return InventoryPage(driver)


@pytest.fixture
def cart_page(driver) -> CartPage:
    return CartPage(driver)


@pytest.fixture
def checkout_step_one_page(driver) -> CheckoutStepOnePage:
    return CheckoutStepOnePage(driver)


@pytest.fixture
def checkout_step_two_page(driver) -> CheckoutStepTwoPage:
    return CheckoutStepTwoPage(driver)


@pytest.fixture
def checkout_complete_page(driver) -> CheckoutCompletePage:
    return CheckoutCompletePage(driver)
