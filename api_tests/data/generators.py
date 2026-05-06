import random

from faker import Faker

fake = Faker()


class PetDataGenerator:
    STATUS_OPTIONS = ["available", "pending", "sold"]

    @staticmethod
    def generate() -> dict:
        return {
            "id": random.randint(100_000, 999_999),
            "name": fake.first_name(),
            "status": random.choice(PetDataGenerator.STATUS_OPTIONS),
            "photoUrls": [fake.image_url()],
            "category": {
                "id": random.randint(1, 10),
                "name": fake.word(),
            },
            "tags": [
                {"id": random.randint(1, 100), "name": fake.word()}
            ],
        }

    @staticmethod
    def generate_update(pet_id: int) -> dict:
        data = PetDataGenerator.generate()
        data["id"] = pet_id
        data["name"] = f"Updated_{fake.first_name()}"
        return data


class UserDataGenerator:
    @staticmethod
    def generate() -> dict:
        first = fake.first_name()
        last = fake.last_name()
        return {
            "id": random.randint(100_000, 999_999),
            "username": f"{first.lower()}{random.randint(100, 9999)}",
            "firstName": first,
            "lastName": last,
            "email": fake.email(),
            "password": fake.password(length=12),
            "phone": fake.phone_number()[:15],
            "userStatus": 1,
        }


class OrderDataGenerator:
    @staticmethod
    def generate(pet_id: int) -> dict:
        return {
            "id": random.randint(100_000, 999_999),
            "petId": pet_id,
            "quantity": random.randint(1, 5),
            "shipDate": "2025-06-01T12:00:00.000Z",
            "status": "placed",
            "complete": True,
        }
