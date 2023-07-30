from pydantic import BaseModel
from typing import List
from datetime import date

from .meal import Meal


class Diary(BaseModel):
    """Diary represents user diary for given day"""

    id: int
    date: date
    meals: List[Meal]
    calories: float
    protein: float
    carb: float
    fat: float
    fiber: float

    class Config:
        from_attributes = True
