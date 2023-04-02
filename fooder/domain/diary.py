from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload
from sqlalchemy import ForeignKey, Integer, Date
from sqlalchemy import select
from sqlalchemy.sql.selectable import Select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional

from .base import Base, CommonMixin
from .meal import Meal
from .entry import Entry


class Diary(Base, CommonMixin):
    """Diary represents user diary for given day"""

    meals: Mapped[list[Meal]] = relationship(lazy="selectin", order_by=Meal.order)
    date: Mapped[date] = mapped_column(Date)
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))

    @property
    def calories(self) -> float:
        """calories.

        :rtype: float
        """
        return sum(meal.calories for meal in self.meals)

    @property
    def protein(self) -> float:
        """protein.

        :rtype: float
        """
        return sum(meal.protein for meal in self.meals)

    @property
    def carb(self) -> float:
        """carb.

        :rtype: float
        """
        return sum(meal.carb for meal in self.meals)

    @property
    def fat(self) -> float:
        """fat.

        :rtype: float
        """
        return sum(meal.fat for meal in self.meals)

    @classmethod
    def query(cls, user_id: int) -> Select:
        """get_all."""
        query = (
            select(cls)
            .where(cls.user_id == user_id)
            .options(
                joinedload(cls.meals).joinedload(Meal.entries).joinedload(Entry.product)
            )
        )
        return query

    @classmethod
    async def get_diary(
        cls, session: AsyncSession, user_id: int, date: date
    ) -> "Optional[Diary]":
        """get_diary."""
        query = select(cls).where(cls.user_id == user_id).where(cls.date == date)
        return await session.scalar(query)

    @classmethod
    async def create(cls, session: AsyncSession, user_id: int, date: date) -> "Diary":
        diary = Diary(
            date=date,
            user_id=user_id,
        )
        session.add(diary)

        try:
            await session.flush()
        except Exception:
            raise RuntimeError()

        diary = await cls.get_by_id(session, user_id, diary.id)

        if not diary:
            raise RuntimeError()
        await Meal.create(session, diary.id)
        return diary

    @classmethod
    async def get_by_id(
        cls, session: AsyncSession, user_id: int, id: int
    ) -> "Optional[Diary]":
        """get_by_id."""
        query = (
            select(cls)
            .where(cls.user_id == user_id)
            .where(cls.id == id)
            .options(joinedload(cls.meals))
        )
        return await session.scalar(query)
