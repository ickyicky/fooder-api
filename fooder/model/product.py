from pydantic import BaseModel
from typing import List


class Product(BaseModel):
    """Product."""

    id: int
    name: str
    calories: float
    protein: float
    carb: float
    fat: float

    class Config:
        orm_mode = True


class CreateProductPayload(BaseModel):
    """ProductCreatePayload."""

    name: str
    protein: float
    carb: float
    fat: float


class ListProductPayload(BaseModel):
    """ProductListPayload."""

    products: List[Product]
