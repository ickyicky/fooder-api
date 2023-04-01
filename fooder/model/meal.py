from pydantic import BaseModel
from typing import List, Optional
from .entry import Entry


class Meal(BaseModel):
    """Meal."""

    id: int
    name: str
    order: int
    calories: float
    protein: float
    carb: float
    fat: float
    entries: List[Entry]
    diary_id: int

    class Config:
        orm_mode = True


class CreateMealPayload(BaseModel):
    """CreateMealPayload."""

    name: Optional[str]
    order: int
    diary_id: int
