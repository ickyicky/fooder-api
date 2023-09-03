import pytest
from typing import Callable


@pytest.fixture
def meal_payload_factory() -> Callable[[int, int], dict[str, int | str]]:
    def factory(diary_id: int, order: int) -> dict[str, int | str]:
        return {
            "order": order,
            "diary_id": diary_id,
            "name": f"meal {order}",
        }

    return factory
