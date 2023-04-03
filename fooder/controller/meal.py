from typing import AsyncIterator
from fastapi import HTTPException

from ..model.meal import Meal, CreateMealPayload
from ..domain.meal import Meal as DBMeal
from ..domain.diary import Diary as DBDiary
from .base import AuthorizedController


class CreateMeal(AuthorizedController):
    async def call(self, content: CreateMealPayload) -> Meal:
        async with self.async_session.begin() as session:
            if not await DBDiary.has_permission(
                session, self.user.id, content.diary_id
            ):
                raise HTTPException(status_code=404, detail="not found")

            try:
                meal = await DBMeal.create(
                    session, content.diary_id, content.order, content.name
                )
                return Meal.from_orm(meal)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])
