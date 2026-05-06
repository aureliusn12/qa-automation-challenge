from http import HTTPStatus

from jsonschema import validate

from api_tests.data.generators import UserDataGenerator
from api_tests.schemas.user_schema import USER_SCHEMA


class TestUserCreate:
    def test_create_returns_200(self, user_service):
        payload = UserDataGenerator.generate()
        response = user_service.create(payload)
        assert response.status_code == HTTPStatus.OK

    def test_create_response_has_code(self, user_service):
        payload = UserDataGenerator.generate()
        response = user_service.create(payload)
        data = response.json()
        assert "code" in data or "message" in data

    def test_create_multiple_users_independently(self, user_service):
        first = UserDataGenerator.generate()
        second = UserDataGenerator.generate()
        r1 = user_service.create(first)
        r2 = user_service.create(second)
        assert r1.status_code == HTTPStatus.OK
        assert r2.status_code == HTTPStatus.OK
        user_service.delete(first["username"])
        user_service.delete(second["username"])


class TestUserRead:
    def test_get_by_username_returns_200(self, created_user, user_service):
        response = user_service.get_by_username(created_user["username"])
        assert response.status_code == HTTPStatus.OK

    def test_get_by_username_schema_valid(self, created_user, user_service):
        response = user_service.get_by_username(created_user["username"])
        validate(instance=response.json(), schema=USER_SCHEMA)

    def test_get_by_username_returns_correct_user(self, created_user, user_service):
        response = user_service.get_by_username(created_user["username"])
        assert response.json()["username"] == created_user["username"]

    def test_get_user_email_matches(self, created_user, user_service):
        response = user_service.get_by_username(created_user["username"])
        assert response.json()["email"] == created_user["email"]

    def test_get_nonexistent_user_returns_404(self, user_service):
        response = user_service.get_by_username("nonexistent_qa_user_xyz_99999")
        assert response.status_code == HTTPStatus.NOT_FOUND


class TestUserSession:
    def test_login_valid_credentials_returns_200(self, created_user, user_service):
        response = user_service.login(created_user["username"], created_user["password"])
        assert response.status_code == HTTPStatus.OK

    def test_login_response_contains_session_token(self, created_user, user_service):
        response = user_service.login(created_user["username"], created_user["password"])
        data = response.json()
        assert "message" in data
        assert "logged in" in data["message"].lower()


class TestUserUpdate:
    def test_update_returns_200(self, created_user, user_service):
        updated = UserDataGenerator.generate()
        updated["username"] = created_user["username"]
        response = user_service.update(created_user["username"], updated)
        assert response.status_code == HTTPStatus.OK

    def test_update_email_persists(self, created_user, user_service):
        updated = UserDataGenerator.generate()
        updated["username"] = created_user["username"]
        user_service.update(created_user["username"], updated)

        fetched = user_service.get_by_username(created_user["username"])
        assert fetched.json()["email"] == updated["email"]


class TestUserDelete:
    def test_delete_existing_user_returns_200(self, user_service):
        payload = UserDataGenerator.generate()
        user_service.create(payload)
        response = user_service.delete(payload["username"])
        assert response.status_code == HTTPStatus.OK

    def test_deleted_user_not_found(self, user_service):
        payload = UserDataGenerator.generate()
        user_service.create(payload)
        user_service.delete(payload["username"])

        response = user_service.get_by_username(payload["username"])
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_nonexistent_user_returns_404(self, user_service):
        response = user_service.delete("nonexistent_qa_user_xyz_99999")
        assert response.status_code == HTTPStatus.NOT_FOUND
