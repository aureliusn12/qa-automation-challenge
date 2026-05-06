import logging
import os

import pytest
from dotenv import load_dotenv

from api_tests.data.generators import PetDataGenerator, UserDataGenerator
from api_tests.services.pet_service import PetService
from api_tests.services.store_service import StoreService
from api_tests.services.user_service import UserService
from api_tests.utils.request_helper import RequestHelper

load_dotenv()

logger = logging.getLogger(__name__)

API_BASE_URL = os.getenv("API_BASE_URL", "https://petstore.swagger.io/v2")


@pytest.fixture(scope="session")
def request_helper() -> RequestHelper:
    return RequestHelper(base_url=API_BASE_URL)


@pytest.fixture(scope="session")
def pet_service(request_helper) -> PetService:
    return PetService(request_helper)


@pytest.fixture(scope="session")
def user_service(request_helper) -> UserService:
    return UserService(request_helper)


@pytest.fixture(scope="session")
def store_service(request_helper) -> StoreService:
    return StoreService(request_helper)


@pytest.fixture
def created_pet(pet_service) -> dict:
    pet_data = PetDataGenerator.generate()
    response = pet_service.create(pet_data)
    assert response.status_code == 200, f"Pet creation failed: {response.text}"
    pet = response.json()
    logger.info("Test pet created — id=%s", pet["id"])
    yield pet
    pet_service.delete(pet["id"])
    logger.info("Test pet cleaned up — id=%s", pet["id"])


@pytest.fixture
def created_user(user_service) -> dict:
    user_data = UserDataGenerator.generate()
    response = user_service.create(user_data)
    assert response.status_code == 200, f"User creation failed: {response.text}"
    logger.info("Test user created — username=%s", user_data["username"])
    yield user_data
    user_service.delete(user_data["username"])
    logger.info("Test user cleaned up — username=%s", user_data["username"])
