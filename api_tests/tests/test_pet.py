from http import HTTPStatus

from jsonschema import validate

from api_tests.data.generators import PetDataGenerator
from api_tests.schemas.pet_schema import PET_SCHEMA


class TestPetCreate:
    def test_create_returns_200(self, pet_service):
        payload = PetDataGenerator.generate()
        response = pet_service.create(payload)
        assert response.status_code == HTTPStatus.OK

    def test_create_response_schema(self, pet_service):
        payload = PetDataGenerator.generate()
        response = pet_service.create(payload)
        validate(instance=response.json(), schema=PET_SCHEMA)

    def test_create_name_matches_payload(self, pet_service):
        payload = PetDataGenerator.generate()
        response = pet_service.create(payload)
        assert response.json()["name"] == payload["name"]

    def test_create_status_matches_payload(self, pet_service):
        payload = PetDataGenerator.generate()
        response = pet_service.create(payload)
        assert response.json()["status"] == payload["status"]

    def test_create_returns_integer_id(self, pet_service):
        payload = PetDataGenerator.generate()
        response = pet_service.create(payload)
        assert isinstance(response.json()["id"], int)


class TestPetRead:
    def test_get_by_id_returns_200(self, created_pet, pet_service):
        response = pet_service.get_by_id(created_pet["id"])
        assert response.status_code == HTTPStatus.OK

    def test_get_by_id_returns_correct_pet(self, created_pet, pet_service):
        response = pet_service.get_by_id(created_pet["id"])
        assert response.json()["id"] == created_pet["id"]

    def test_get_by_id_schema_valid(self, created_pet, pet_service):
        response = pet_service.get_by_id(created_pet["id"])
        validate(instance=response.json(), schema=PET_SCHEMA)

    def test_get_nonexistent_pet_returns_404(self, pet_service):
        response = pet_service.get_by_id(9_999_999_999)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_find_by_status_available_returns_200(self, pet_service):
        response = pet_service.find_by_status("available")
        assert response.status_code == HTTPStatus.OK

    def test_find_by_status_returns_list(self, pet_service):
        response = pet_service.find_by_status("available")
        assert isinstance(response.json(), list)

    def test_find_by_status_filters_correctly(self, pet_service):
        response = pet_service.find_by_status("pending")
        assert response.status_code == HTTPStatus.OK
        assert all(p.get("status") == "pending" for p in response.json())

    def test_find_by_invalid_status(self, pet_service):
        response = pet_service.find_by_status("unknown_status")
        assert response.status_code in (HTTPStatus.BAD_REQUEST, HTTPStatus.OK)


class TestPetUpdate:
    def test_update_returns_200(self, created_pet, pet_service):
        payload = PetDataGenerator.generate_update(created_pet["id"])
        response = pet_service.update(payload)
        assert response.status_code == HTTPStatus.OK

    def test_update_name_changes(self, created_pet, pet_service):
        payload = PetDataGenerator.generate_update(created_pet["id"])
        response = pet_service.update(payload)
        assert response.json()["name"] == payload["name"]

    def test_update_schema_valid(self, created_pet, pet_service):
        payload = PetDataGenerator.generate_update(created_pet["id"])
        response = pet_service.update(payload)
        validate(instance=response.json(), schema=PET_SCHEMA)


class TestPetDelete:
    def test_delete_existing_pet_returns_200(self, pet_service):
        payload = PetDataGenerator.generate()
        created = pet_service.create(payload)
        assert created.status_code == HTTPStatus.OK
        pet_id = created.json()["id"]

        response = pet_service.delete(pet_id)
        assert response.status_code == HTTPStatus.OK

    def test_deleted_pet_not_found(self, pet_service):
        payload = PetDataGenerator.generate()
        created = pet_service.create(payload)
        pet_id = created.json()["id"]
        pet_service.delete(pet_id)

        response = pet_service.get_by_id(pet_id)
        assert response.status_code == HTTPStatus.NOT_FOUND

    def test_delete_nonexistent_pet_returns_404(self, pet_service):
        response = pet_service.delete(9_999_999_999)
        assert response.status_code == HTTPStatus.NOT_FOUND
