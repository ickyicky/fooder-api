from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy import ForeignKey, Integer, DateTime
from datetime import datetime

from .base import Base, CommonMixin
from .product import Product
from .entry import Entry


class PresetEntry(Base, CommonMixin):
    """Entry."""

    grams: Mapped[float]
    product_id: Mapped[int] = mapped_column(Integer, ForeignKey("product.id"))
    product: Mapped[Product] = relationship(lazy="selectin")
    preset_id: Mapped[int] = mapped_column(Integer, ForeignKey("preset.id"))
    last_changed: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

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
        self,
        session: AsyncSession,
        preset_id: int,
        entry: Entry,
    ) -> None:
        pentry = PresetEntry(
            preset_id=preset_id,
            product_id=entry.product_id,
            grams=entry.grams,
        )
        session.add(pentry)

        try:
            await session.flush()
        except IntegrityError:
            raise AssertionError("preset or product does not exist")
