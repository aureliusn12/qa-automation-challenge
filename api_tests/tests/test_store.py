from http import HTTPStatus

from jsonschema import validate

from api_tests.data.generators import OrderDataGenerator
from api_tests.schemas.store_schema import INVENTORY_SCHEMA, ORDER_SCHEMA


class TestStoreInventory:
    def test_get_inventory_returns_200(self, store_service):
        response = store_service.get_inventory()
        assert response.status_code == HTTPStatus.OK

    def test_get_inventory_schema_valid(self, store_service):
        response = store_service.get_inventory()
        validate(instance=response.json(), schema=INVENTORY_SCHEMA)

    def test_inventory_is_non_empty_dict(self, store_service):
        response = store_service.get_inventory()
        data = response.json()
        assert isinstance(data, dict)
        assert len(data) > 0

    def test_inventory_values_are_integers(self, store_service):
        response = store_service.get_inventory()
        for key, value in response.json().items():
            assert isinstance(value, int), f"Unexpected type for key '{key}': {type(value)}"


class TestStoreOrder:
    def test_place_order_returns_200(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        response = store_service.place_order(payload)
        assert response.status_code == HTTPStatus.OK

    def test_place_order_schema_valid(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        response = store_service.place_order(payload)
        validate(instance=response.json(), schema=ORDER_SCHEMA)

    def test_place_order_status_is_placed(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        response = store_service.place_order(payload)
        assert response.json()["status"] == "placed"

    def test_place_order_pet_id_matches(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        response = store_service.place_order(payload)
        assert response.json()["petId"] == created_pet["id"]

    def test_get_order_by_id_returns_200(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        created = store_service.place_order(payload)
        order_id = created.json()["id"]

        response = store_service.get_order(order_id)
        assert response.status_code == HTTPStatus.OK

    def test_get_order_data_matches(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        created = store_service.place_order(payload)
        order_id = created.json()["id"]

        response = store_service.get_order(order_id)
        assert response.json()["id"] == order_id
        assert response.json()["petId"] == created_pet["id"]

    def test_get_order_schema_valid(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        created = store_service.place_order(payload)
        order_id = created.json()["id"]

        response = store_service.get_order(order_id)
        validate(instance=response.json(), schema=ORDER_SCHEMA)

    def test_get_nonexistent_order_returns_404(self, store_service):
        response = store_service.get_order(9_999_999_999)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_order_returns_200(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        created = store_service.place_order(payload)
        order_id = created.json()["id"]

        response = store_service.delete_order(order_id)
        assert response.status_code == HTTPStatus.OK

    def test_deleted_order_not_found(self, created_pet, store_service):
        payload = OrderDataGenerator.generate(created_pet["id"])
        created = store_service.place_order(payload)
        order_id = created.json()["id"]
        store_service.delete_order(order_id)

        response = store_service.get_order(order_id)
        assert response.status_code == HTTPStatus.NOT_FOUND
