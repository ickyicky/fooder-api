from datetime import date
from fastapi import HTTPException

from ..model.diary import Diary
from ..domain.diary import Diary as DBDiary
from ..domain.meal import Meal as DBMeal
from .base import AuthorizedController


class GetDiary(AuthorizedController):
    async def call(self, date: date) -> Diary:
        async with self.async_session() as session:
            diary = await DBDiary.get_diary(session, self.user.id, date)

            if diary is not None:
                return Diary.from_orm(diary)
            else:
                try:
                    await DBDiary.create(session, self.user.id, date)
                    await session.commit()
                    return Diary.from_orm(
                        await DBDiary.get_diary(session, self.user.id, date)
                    )
                except AssertionError as e:
                    raise HTTPException(status_code=400, detail=e.args[0])
