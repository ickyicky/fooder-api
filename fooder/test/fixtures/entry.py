import pytest
from typing import Callable


@pytest.fixture
def entry_payload_factory() -> Callable[[int, int, float], dict[str, int | float]]:
    def factory(meal_id: int, product_id: int, grams: float) -> dict[str, int | float]:
        return {
            "meal_id": meal_id,
            "product_id": product_id,
            "grams": grams,
        }

    return factory
