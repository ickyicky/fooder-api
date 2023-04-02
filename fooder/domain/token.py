from sqlalchemy.orm import relationship, Mapped, mapped_column, joinedload
from sqlalchemy import ForeignKey, Integer, Date
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import date
from typing import Optional

from .base import Base, CommonMixin
from .meal import Meal


class RefreshToken(Base, CommonMixin):
    """Diary represents user diary for given day"""

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"), unique=True)
    token: Mapped[str]

    @classmethod
    async def get_token(
        cls,
        session: AsyncSession,
        user_id: int,
    ) -> "Optional[RefreshToken]":
        """get_token."""
        query = select(cls).where(cls.user_id == user_id)
        return await session.scalar(query)

    @classmethod
    async def create(
        cls, session: AsyncSession, user_id: int, token: str
    ) -> "RefreshToken":
        """create.

        :param session:
        :type session: AsyncSession
        :param user_id:
        :type user_id: int
        :param token:
        :type token: str
        :rtype: "RefreshToken"
        """
        existing = await cls.get_token(session, user_id)

        if existing:
            existing.token = token
            return existing

        token = cls(
            user_id=user_id,
            token=token,
        )
        session.add(token)

        try:
            await session.flush()
        except Exception:
            raise AssertionError("invalid token")

        return token
