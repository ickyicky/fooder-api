import pytest
import uuid
from typing import Callable


@pytest.fixture
def product_payload_factory() -> Callable[[], dict[str, str | float]]:
    def factory() -> dict[str, str | float]:
        return {
            "name": "test" + str(uuid.uuid4().hex),
            "protein": 1.0,
            "carb": 1.0,
            "fat": 1.0,
            "fiber": 1.0,
        }

    return factory


@pytest.fixture
def product_payload(product_payload_factory) -> dict[str, str | float]:
    return product_payload_factory()
