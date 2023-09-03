import pytest
from typing import Callable
import uuid


@pytest.fixture
def user_payload() -> dict[str, str]:
    return {
        "username": "test",
        "password": "test",
    }


@pytest.fixture
def user_payload_factory(user_payload) -> Callable[[], dict[str, str]]:
    def factory() -> dict[str, str]:
        return {
            "username": "test" + str(uuid.uuid4().hex),
            "password": "test",
        }

    return factory
