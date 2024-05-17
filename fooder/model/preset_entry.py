from pydantic import BaseModel

from .product import Product


class PresetEntry(BaseModel):
    """PresetEntry."""

    id: int
    grams: float
    product: Product
    preset_id: int
    calories: float
    protein: float
    carb: float
    fat: float
    fiber: float

    class Config:
        from_attributes = True
