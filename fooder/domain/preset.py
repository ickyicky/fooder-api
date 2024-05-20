from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import ForeignKey, Integer, select

from .base import Base, CommonMixin
from .preset_entry import PresetEntry
from typing import AsyncIterator, Optional, TYPE_CHECKING


if TYPE_CHECKING:
    from .meal import Meal


class Preset(Base, CommonMixin):
    """Preset."""

    name: Mapped[str]
    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    entries: Mapped[list[PresetEntry]] = relationship(
        lazy="selectin", order_by=PresetEntry.last_changed
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

    @property
    def fiber(self) -> float:
        """fiber.

        :rtype: float
        """
        return sum(entry.fiber for entry in self.entries)

    @classmethod
    async def create(
        cls, session: AsyncSession, user_id: int, name: str, meal: "Meal"
    ) -> "Preset":
        preset = Preset(user_id=user_id, name=name)

        session.add(preset)

        try:
            await session.flush()
        except Exception:
            raise RuntimeError()

        for entry in meal.entries:
            await PresetEntry.create(session, preset.id, entry)

        db_preset = await cls.get(session, user_id, preset.id)

        if not db_preset:
            raise RuntimeError()

        return db_preset

    @classmethod
    async def list_all(
        cls,
        session: AsyncSession,
        user_id: int,
        offset: int,
        limit: int,
        q: Optional[str] = None,
    ) -> AsyncIterator["Preset"]:
        query = select(cls).filter(cls.user_id == user_id)

        if q:
            query = query.filter(cls.name.ilike(f"%{q.lower()}%"))

        query = query.offset(offset).limit(limit)
        stream = await session.stream_scalars(query.order_by(cls.id))
        async for row in stream:
            yield row

    @classmethod
    async def get(
        cls, session: AsyncSession, user_id: int, preset_id: int
    ) -> "Optional[Preset]":
        """get."""
        query = (
            select(cls)
            .where(cls.id == preset_id)
            .where(cls.user_id == user_id)
            .options(joinedload(cls.entries).joinedload(PresetEntry.product))
        )
        return await session.scalar(query)

    async def delete(self, session: AsyncSession) -> None:
        for entry in self.entries:
            await session.delete(entry)
        await session.delete(self)
        await session.flush()
