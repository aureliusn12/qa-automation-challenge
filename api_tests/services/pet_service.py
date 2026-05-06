import requests

from api_tests.services.base_service import BaseService


class PetService(BaseService):
    _BASE = "/pet"

    def create(self, payload: dict) -> requests.Response:
        return self.client.post(self._BASE, payload)

    def get_by_id(self, pet_id: int) -> requests.Response:
        return self.client.get(f"{self._BASE}/{pet_id}")

    def update(self, payload: dict) -> requests.Response:
        return self.client.put(self._BASE, payload)

    def delete(self, pet_id: int) -> requests.Response:
        return self.client.delete(f"{self._BASE}/{pet_id}")

    def find_by_status(self, status: str) -> requests.Response:
        return self.client.get(f"{self._BASE}/findByStatus", params={"status": status})
