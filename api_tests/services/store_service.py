import requests

from api_tests.services.base_service import BaseService


class StoreService(BaseService):
    _BASE = "/store"

    def get_inventory(self) -> requests.Response:
        return self.client.get(f"{self._BASE}/inventory")

    def place_order(self, payload: dict) -> requests.Response:
        return self.client.post(f"{self._BASE}/order", payload)

    def get_order(self, order_id: int) -> requests.Response:
        return self.client.get(f"{self._BASE}/order/{order_id}")

    def delete_order(self, order_id: int) -> requests.Response:
        return self.client.delete(f"{self._BASE}/order/{order_id}")
