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
    fiber: float
    entries: List[Entry]
    diary_id: int

    class Config:
        from_attributes = True


class CreateMealPayload(BaseModel):
    """CreateMealPayload."""

    name: Optional[str]
    diary_id: int


class SaveMealPayload(BaseModel):
    """SaveMealPayload."""

    name: Optional[str]


class CreateMealFromPresetPayload(BaseModel):
    """CreateMealPayload."""

    name: Optional[str]
    diary_id: int
    preset_id: int
