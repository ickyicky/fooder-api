from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload
from sqlalchemy import ForeignKey, Integer, DateTime, Boolean
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, update
from datetime import datetime
from typing import Optional

from .base import Base, CommonMixin
from .product import Product


class Entry(Base, CommonMixin):
    """Entry."""

    grams: Mapped[float]
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"))
    product: Mapped[Product] = relationship(lazy="selectin")
    meal_id: Mapped[int] = mapped_column(Integer, ForeignKey("meal.id"))
    last_changed: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )
    processed: Mapped[bool] = mapped_column(Boolean, default=False)

    @property
    def amount(self) -> float:
        """amount.

        :rtype: float
        """
        return self.grams / 100

    @property
    def calories(self) -> float:
        """calories.

        :rtype: float
        """
        return self.amount * self.product.calories

    @property
    def protein(self) -> float:
        """protein.

        :rtype: float
        """
        return self.amount * self.product.protein

    @property
    def carb(self) -> float:
        """carb.

        :rtype: float
        """
        return self.amount * self.product.carb

    @property
    def fat(self) -> float:
        """fat.

        :rtype: float
        """
        return self.amount * self.product.fat

    @property
    def fiber(self) -> float:
        """fiber.

        :rtype: float
        """
        return self.amount * self.product.fiber

    @classmethod
    async def create(
        cls, session: AsyncSession, meal_id: int, product_id: int, grams: float
    ) -> "Entry":
        """create."""
        assert grams > 0, "grams must be greater than 0"
        entry = Entry(
            meal_id=meal_id,
            product_id=product_id,
            grams=grams,
        )
        session.add(entry)

        try:
            await session.flush()
        except IntegrityError:
            raise AssertionError("meal or product does not exist")

        db_entry = await cls._get_by_id(session, entry.id)
        if not db_entry:
            raise RuntimeError()
        return db_entry

    async def update(
        self,
        session: AsyncSession,
        meal_id: Optional[int],
        product_id: Optional[int],
        grams: Optional[float],
    ) -> None:
        """update."""
        if grams is not None:
            assert grams > 0, "grams must be greater than 0"
            self.grams = grams

        if meal_id is not None:
            self.meal_id = meal_id
            try:
                await session.flush()
            except IntegrityError:
                raise AssertionError("meal does not exist")

        if product_id is not None:
            self.product_id = product_id
            try:
                await session.flush()
            except IntegrityError:
                raise AssertionError("product does not exist")

    @classmethod
    async def _get_by_id(cls, session: AsyncSession, id: int) -> "Optional[Entry]":
        """get_by_id."""
        query = select(cls).where(cls.id == id).options(joinedload(cls.product))
        return await session.scalar(query.order_by(cls.id))

    @classmethod
    async def get_by_id(
        cls, session: AsyncSession, user_id: int, id: int
    ) -> "Optional[Entry]":
        """get_by_id."""
        from .diary import Diary
        from .meal import Meal

        query = (
            select(cls)
            .where(cls.id == id)
            .join(
                Meal,
            )
            .join(
                Diary,
            )
            .where(
                Diary.user_id == user_id,
            )
            .options(joinedload(cls.product))
        )
        return await session.scalar(query.order_by(cls.id))

    async def delete(self, session) -> None:
        """delete."""
        await session.delete(self)
        await session.flush()

    @classmethod
    async def mark_processed(
        cls,
        session: AsyncSession,
    ) -> None:
        stmt = update(cls).where(cls.processed == False).values(processed=True)

        await session.execute(stmt)
