from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import select, BigInteger, func, update
from sqlalchemy.ext.asyncio import AsyncSession
from typing import AsyncIterator, Optional

from .base import Base, CommonMixin


class Product(Base, CommonMixin):
    """Product."""

    name: Mapped[str]

    protein: Mapped[float]
    carb: Mapped[float]
    fat: Mapped[float]
    fiber: Mapped[float]
    hard_coded_calories: Mapped[Optional[float]]
    barcode: Mapped[Optional[str]]

    usage_count_cached: Mapped[int] = mapped_column(
        BigInteger,
        default=0,
        nullable=False,
    )

    @property
    def calories(self) -> float:
        """calories.

        :rtype: float
        """
        if self.hard_coded_calories:
            return self.hard_coded_calories

        return self.protein * 4 + self.carb * 4 + self.fat * 9 + self.fiber * 2

    @classmethod
    async def list_all(
        cls,
        session: AsyncSession,
        offset: int,
        limit: int,
        q: Optional[str] = None,
    ) -> AsyncIterator["Product"]:
        query = select(cls)

        if q:
            q_list = q.split()
            qq = "%" + "%".join(q_list) + "%"
            query = query.filter(cls.name.ilike(f"%{qq.lower()}%"))

        query = query.offset(offset).limit(limit)
        stream = await session.stream_scalars(
            query.order_by(cls.usage_count_cached.desc())
        )
        async for row in stream:
            yield row

    @classmethod
    async def get_by_barcode(
        cls, session: AsyncSession, barcode: str
    ) -> Optional["Product"]:
        query = select(cls).where(cls.barcode == barcode)
        return await session.scalar(query)

    @classmethod
    async def create(
        cls,
        session: AsyncSession,
        name: str,
        carb: float,
        protein: float,
        fat: float,
        fiber: float,
        hard_coded_calories: Optional[float] = None,
        barcode: Optional[str] = None,
    ) -> "Product":
        # validation here
        assert carb <= 100, "carb must be less than 100"
        assert protein <= 100, "protein must be less than 100"
        assert fat <= 100, "fat must be less than 100"
        assert fiber <= 100, "fiber must be less than 100"
        assert carb >= 0, "carb must be greater than 0"
        assert protein >= 0, "protein must be greater than 0"
        assert fat >= 0, "fat must be greater than 0"
        assert fiber >= 0, "fiber must be greater than 0"
        assert carb + protein + fat <= 100, "total must be less than 100"

        # to avoid duplicates in the database keep name as lower
        name = name.lower()

        # check if product already exists
        if barcode is not None:
            query = select(cls).where((cls.name == name) | (cls.barcode == barcode))
        else:
            query = select(cls).where(cls.name == name)

        existing_product = await session.scalar(query)
        assert existing_product is None, "product already exists"

        product = Product(
            name=name,
            protein=protein,
            carb=carb,
            fat=fat,
            fiber=fiber,
            hard_coded_calories=hard_coded_calories,
            barcode=barcode,
        )

        session.add(product)
        await session.flush()
        return product

    @classmethod
    async def cache_usage_data(
        cls,
        session: AsyncSession,
    ) -> None:
        from .entry import Entry

        stmt = (
            update(cls)
            .where(
                cls.id.in_(
                    select(Entry.product_id).where(Entry.processed == False).distinct()
                )
            )
            .values(
                usage_count_cached=select(func.count(Entry.id)).where(
                    Entry.product_id == cls.id,
                    Entry.processed == False,
                )
            )
        )

        await session.execute(stmt)
        await Entry.mark_processed(session)
