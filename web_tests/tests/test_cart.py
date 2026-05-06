from web_tests.data.test_data import PRODUCTS
from web_tests.pages.cart_page import CartPage
from web_tests.pages.inventory_page import InventoryPage


class TestCart:
    def test_add_single_product_updates_badge(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product(PRODUCTS[0])
        assert inventory.get_cart_count() == 1

    def test_add_multiple_products_updates_badge(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product(PRODUCTS[0]).add_product(PRODUCTS[1])
        assert inventory.get_cart_count() == 2

    def test_remove_product_decrements_badge(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product(PRODUCTS[0]).add_product(PRODUCTS[1])
        inventory.remove_product(PRODUCTS[0])
        assert inventory.get_cart_count() == 1

    def test_cart_page_shows_correct_item_count(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product(PRODUCTS[0]).add_product(PRODUCTS[1])
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert cart.is_on_page()
        assert cart.get_item_count() == 2

    def test_cart_contains_added_product_name(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        inventory.add_product(PRODUCTS[0])
        inventory.go_to_cart()

        cart = CartPage(logged_in_driver)
        assert PRODUCTS[0] in cart.get_item_names()

    def test_empty_cart_badge_not_visible(self, logged_in_driver):
        inventory = InventoryPage(logged_in_driver)
        assert inventory.get_cart_count() == 0
