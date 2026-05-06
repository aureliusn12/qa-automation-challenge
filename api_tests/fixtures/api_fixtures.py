import pytest

from api_tests.data.generators import OrderDataGenerator, PetDataGenerator, UserDataGenerator


@pytest.fixture
def pet_payload() -> dict:
    return PetDataGenerator.generate()


@pytest.fixture
def user_payload() -> dict:
    return UserDataGenerator.generate()


@pytest.fixture
def order_payload(created_pet) -> dict:
    return OrderDataGenerator.generate(created_pet["id"])
