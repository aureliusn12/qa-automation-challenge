from web_tests.data.test_data import PRODUCTS, VALID_CUSTOMER
from web_tests.pages.cart_page import CartPage
from web_tests.pages.checkout_complete_page import CheckoutCompletePage
from web_tests.pages.checkout_step_one_page import CheckoutStepOnePage
from web_tests.pages.checkout_step_two_page import CheckoutStepTwoPage
from web_tests.pages.inventory_page import InventoryPage


class TestCheckoutE2E:
    def test_full_purchase_flow(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product(PRODUCTS[0]).add_product(PRODUCTS[1])
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert cart.is_on_page()
        assert cart.get_item_count() == 2
        cart.proceed_to_checkout()

        step_one = CheckoutStepOnePage(logged_in_driver)
        assert step_one.is_on_page()
        step_one.fill_customer_info(
            VALID_CUSTOMER.first_name,
            VALID_CUSTOMER.last_name,
            VALID_CUSTOMER.zip_code,
        ).continue_to_overview()

        step_two = CheckoutStepTwoPage(logged_in_driver)
        assert step_two.is_on_page()
        assert step_two.get_item_count() == 2
        step_two.finish_purchase()

        complete = CheckoutCompletePage(logged_in_driver)
        assert complete.is_on_page()
        assert complete.is_order_confirmed()

    def test_confirmation_header_text(self, logged_in_driver):
        InventoryPage(logged_in_driver).add_product(PRODUCTS[0]).go_to_cart()
        CartPage(logged_in_driver).proceed_to_checkout()
        CheckoutStepOnePage(logged_in_driver).fill_customer_info(
            VALID_CUSTOMER.first_name, VALID_CUSTOMER.last_name, VALID_CUSTOMER.zip_code
        ).continue_to_overview()
        CheckoutStepTwoPage(logged_in_driver).finish_purchase()

        complete = CheckoutCompletePage(logged_in_driver)
        assert complete.get_confirmation_header() == CheckoutCompletePage.EXPECTED_HEADER

    def test_checkout_requires_first_name(self, logged_in_driver):
        InventoryPage(logged_in_driver).add_product(PRODUCTS[0]).go_to_cart()
        CartPage(logged_in_driver).proceed_to_checkout()

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_customer_info("", VALID_CUSTOMER.last_name, VALID_CUSTOMER.zip_code)
        step_one.continue_to_overview()
        assert step_one.is_error_displayed()

    def test_checkout_requires_last_name(self, logged_in_driver):
        InventoryPage(logged_in_driver).add_product(PRODUCTS[0]).go_to_cart()
        CartPage(logged_in_driver).proceed_to_checkout()

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_customer_info(VALID_CUSTOMER.first_name, "", VALID_CUSTOMER.zip_code)
        step_one.continue_to_overview()
        assert step_one.is_error_displayed()

    def test_checkout_requires_zip_code(self, logged_in_driver):
        InventoryPage(logged_in_driver).add_product(PRODUCTS[0]).go_to_cart()
        CartPage(logged_in_driver).proceed_to_checkout()

        step_one = CheckoutStepOnePage(logged_in_driver)
        step_one.fill_customer_info(VALID_CUSTOMER.first_name, VALID_CUSTOMER.last_name, "")
        step_one.continue_to_overview()
        assert step_one.is_error_displayed()

    def test_overview_shows_price_summary(self, logged_in_driver):
        InventoryPage(logged_in_driver).add_product(PRODUCTS[0]).go_to_cart()
        CartPage(logged_in_driver).proceed_to_checkout()
        CheckoutStepOnePage(logged_in_driver).fill_customer_info(
            VALID_CUSTOMER.first_name, VALID_CUSTOMER.last_name, VALID_CUSTOMER.zip_code
        ).continue_to_overview()

        step_two = CheckoutStepTwoPage(logged_in_driver)
        assert "Item total" in step_two.get_item_total_text()
        assert "Total" in step_two.get_total_text()
