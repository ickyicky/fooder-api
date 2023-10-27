from fastapi import APIRouter, Depends, Request
from ..model.meal import (
    Meal,
    CreateMealPayload,
    SaveMealPayload,
    CreateMealFromPresetPayload,
)
from ..controller.meal import CreateMeal, SaveMeal, CreateMealFromPreset


router = APIRouter(tags=["meal"])


@router.post("", response_model=Meal)
async def create_meal(
    request: Request,
    data: CreateMealPayload,
    contoller: CreateMeal = Depends(CreateMeal),
):
    return await contoller.call(data)


@router.post("/{meal_id}/save")
async def save_meal(
    request: Request,
    meal_id: int,
    data: SaveMealPayload,
    contoller: SaveMeal = Depends(SaveMeal),
):
    await contoller.call(meal_id, data)


@router.post("/from_preset", response_model=Meal)
async def create_meal_from_preset(
    request: Request,
    data: CreateMealFromPresetPayload,
    contoller: CreateMealFromPreset = Depends(CreateMealFromPreset),
):
    return await contoller.call(data)
