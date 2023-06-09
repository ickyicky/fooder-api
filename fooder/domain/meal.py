from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload
from sqlalchemy import ForeignKey, Integer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from typing import Optional

from .base import Base, CommonMixin
from .entry import Entry


class Meal(Base, CommonMixin):
    """Meal."""

    name: Mapped[str]
    order: Mapped[int]
    diary_id: Mapped[int] = mapped_column(Integer, ForeignKey("diary.id"))
    entries: Mapped[list[Entry]] = relationship(
        lazy="selectin", order_by=Entry.last_changed
    )

    @property
    def calories(self) -> float:
        """calories.

        :rtype: float
        """
        return sum(entry.calories for entry in self.entries)

    @property
    def protein(self) -> float:
        """protein.

        :rtype: float
        """
        return sum(entry.protein for entry in self.entries)

    @property
    def carb(self) -> float:
        """carb.

        :rtype: float
        """
        return sum(entry.carb for entry in self.entries)

    @property
    def fat(self) -> float:
        """fat.

        :rtype: float
        """
        return sum(entry.fat for entry in self.entries)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        diary_id: int,
        order: int = 0,
        name: Optional[str] = None,
    ) -> "Meal":
        # check if order already exists in diary
        query = select(cls).where(cls.diary_id == diary_id).where(cls.order == order)
        existing_meal = await session.scalar(query)
        assert existing_meal is None, "order already exists in diary"

        if name is None:
            name = f"Meal {order}"
        meal = Meal(diary_id=diary_id, name=name, order=order)
        session.add(meal)

        try:
            await session.flush()
        except IntegrityError:
            raise AssertionError("diary does not exist")

        meal = await cls._get_by_id(session, meal.id)
        if not meal:
            raise RuntimeError()
        return meal

    @classmethod
    async def _get_by_id(cls, session: AsyncSession, id: int) -> "Optional[Meal]":
        """get_by_id."""
        query = select(cls).where(cls.id == id).options(joinedload(cls.entries))
        return await session.scalar(query.order_by(cls.id))

    @classmethod
    async def get_by_id(
        cls, session: AsyncSession, user_id: int, id: int
    ) -> "Optional[Meal]":
        """get_by_id."""
        from .diary import Diary

        query = (
            select(cls)
            .where(cls.id == id)
            .join(Diary)
            .where(Diary.user_id == user_id)
            .options(joinedload(cls.entries))
        )
        return await session.scalar(query.order_by(cls.id))
