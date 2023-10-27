from fastapi import APIRouter, Depends, Request
from ..model.preset import Preset
from ..model.meal import (
    Meal,
    CreateMealPayload,
    SaveMealPayload,
    CreateMealFromPresetPayload,
)
from ..controller.meal import CreateMeal, SaveMeal, CreateMealFromPreset, DeleteMeal


router = APIRouter(tags=["meal"])


@router.post("", response_model=Meal)
async def create_meal(
    request: Request,
    data: CreateMealPayload,
    contoller: CreateMeal = Depends(CreateMeal),
):
    return await contoller.call(data)


@router.post("/{meal_id}/save", response_model=Preset)
async def save_meal(
    request: Request,
    meal_id: int,
    data: SaveMealPayload,
    contoller: SaveMeal = Depends(SaveMeal),
):
    return await contoller.call(meal_id, data)


@router.delete("/{meal_id}")
async def delete_meal(
    request: Request,
    meal_id: int,
    contoller: DeleteMeal = Depends(DeleteMeal),
):
    return await contoller.call(meal_id)


@router.post("/from_preset", response_model=Meal)
async def create_meal_from_preset(
    request: Request,
    data: CreateMealFromPresetPayload,
    contoller: CreateMealFromPreset = Depends(CreateMealFromPreset),
):
    return await contoller.call(data)
