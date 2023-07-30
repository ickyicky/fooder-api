from pydantic import BaseModel
from typing import Optional

from .product import Product


class Entry(BaseModel):
    """Entry."""

    id: int
    grams: float
    product: Product
    meal_id: int
    calories: float
    protein: float
    carb: float
    fat: float
    fiber: float

    class Config:
        from_attributes = True


class CreateEntryPayload(BaseModel):
    """CreateEntryPayload."""

    grams: float
    product_id: int
    meal_id: int


class UpdateEntryPayload(BaseModel):
    """CreateEntryPayload."""

    grams: Optional[float]
    product_id: Optional[int]
    meal_id: Optional[int]
