from fastapi import APIRouter, Depends, Request
from ..model.meal import Meal, CreateMealPayload
from ..controller.meal import CreateMeal


router = APIRouter(tags=["meal"])


@router.post("", response_model=Meal)
async def create_meal(
    request: Request,
    data: CreateMealPayload,
    contoller: CreateMeal = Depends(CreateMeal),
):
    return await contoller.call(data)
