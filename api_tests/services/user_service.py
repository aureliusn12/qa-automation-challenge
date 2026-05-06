import requests

from api_tests.services.base_service import BaseService


class UserService(BaseService):
    _BASE = "/user"

    def create(self, payload: dict) -> requests.Response:
        return self.client.post(self._BASE, payload)

    def get_by_username(self, username: str) -> requests.Response:
        return self.client.get(f"{self._BASE}/{username}")

    def update(self, username: str, payload: dict) -> requests.Response:
        return self.client.put(f"{self._BASE}/{username}", payload)

    def delete(self, username: str) -> requests.Response:
        return self.client.delete(f"{self._BASE}/{username}")

    def login(self, username: str, password: str) -> requests.Response:
        return self.client.get(
            f"{self._BASE}/login",
            params={"username": username, "password": password},
        )
