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


@pytest.fixture
def meal_save_payload() -> Callable[[int], dict[str, str]]:
    def factory(meal_id: int) -> dict[str, str]:
        return {
            "name": "new name",
        }

    return factory


@pytest.fixture
def meal_from_preset() -> Callable[[int, int, int], dict[str, str | int]]:
    def factory(order: int, diary_id: int, preset_id: int) -> dict[str, str | int]:
        return {
            "name": "new name",
            "order": order,
            "diary_id": diary_id,
            "preset_id": preset_id,
        }

    return factory
