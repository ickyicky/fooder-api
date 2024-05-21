from fastapi import HTTPException

from ..model.meal import (
    Meal,
    CreateMealPayload,
    SaveMealPayload,
    CreateMealFromPresetPayload,
)
from ..model.preset import Preset
from ..domain.meal import Meal as DBMeal
from ..domain.diary import Diary as DBDiary
from ..domain.preset import Preset as DBPreset
from .base import AuthorizedController


class CreateMeal(AuthorizedController):
    async def call(self, content: CreateMealPayload) -> Meal:
        async with self.async_session.begin() as session:
            if not await DBDiary.has_permission(
                session, self.user.id, content.diary_id
            ):
                raise HTTPException(status_code=404, detail="not found")

            try:
                meal = await DBMeal.create(session, content.diary_id, content.name)
                return Meal.from_orm(meal)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])


class SaveMeal(AuthorizedController):
    async def call(self, meal_id: int, payload: SaveMealPayload) -> Preset:
        async with self.async_session.begin() as session:
            meal = await DBMeal.get_by_id(session, self.user.id, meal_id)
            if meal is None:
                raise HTTPException(status_code=404, detail="meal not found")

            try:
                return Preset.from_orm(
                    await DBPreset.create(
                        session,
                        user_id=self.user.id,
                        name=payload.name or meal.name,
                        meal=meal,
                    )
                )
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])


class DeleteMeal(AuthorizedController):
    async def call(self, meal_id: int) -> None:
        async with self.async_session.begin() as session:
            meal = await DBMeal.get_by_id(session, self.user.id, meal_id)
            if meal is None:
                raise HTTPException(status_code=404, detail="meal not found")

            try:
                await meal.delete(session)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])


class CreateMealFromPreset(AuthorizedController):
    async def call(self, content: CreateMealFromPresetPayload) -> Meal:
        async with self.async_session.begin() as session:
            if not await DBDiary.has_permission(
                session, self.user.id, content.diary_id
            ):
                raise HTTPException(status_code=404, detail="diary not found")

            preset = await DBPreset.get(session, self.user.id, content.preset_id)

            if preset is None:
                raise HTTPException(status_code=404, detail="preset not found")

            try:
                meal = await DBMeal.create_from_preset(
                    session, content.diary_id, content.name, preset
                )
                return Meal.from_orm(meal)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])
