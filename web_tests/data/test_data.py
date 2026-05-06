from dataclasses import dataclass
from typing import List


@dataclass(frozen=True)
class UserCredentials:
    username: str
    password: str


@dataclass(frozen=True)
class CustomerInfo:
    first_name: str
    last_name: str
    zip_code: str


STANDARD_USER = UserCredentials(username="standard_user", password="secret_sauce")
LOCKED_USER = UserCredentials(username="locked_out_user", password="secret_sauce")
PROBLEM_USER = UserCredentials(username="problem_user", password="secret_sauce")

VALID_CUSTOMER = CustomerInfo(first_name="John", last_name="Doe", zip_code="12345")

PRODUCTS: List[str] = [
    "Sauce Labs Backpack",
    "Sauce Labs Bike Light",
    "Sauce Labs Bolt T-Shirt",
]
