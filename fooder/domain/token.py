from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import ForeignKey, Integer
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .base import Base, CommonMixin


class RefreshToken(Base, CommonMixin):
    """Diary represents user diary for given day"""

    user_id: Mapped[int] = mapped_column(Integer, ForeignKey("user.id"))
    token: Mapped[str]

    @classmethod
    async def get_token(
        cls,
        session: AsyncSession,
        user_id: int,
        token: str,
    ) -> "Optional[RefreshToken]":
        """get_token.

        :param session:
        :type session: AsyncSession
        :param user_id:
        :type user_id: int
        :param token:
        :type token: str
        :rtype: "Optional[RefreshToken]"
        """
        query = select(cls).where(cls.user_id == user_id).where(cls.token == token)
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
        db_token = cls(
            user_id=user_id,
            token=token,
        )
        session.add(db_token)

        try:
            await session.flush()
        except Exception:
            raise AssertionError("invalid token")

        return db_token

    async def delete(self, session: AsyncSession) -> None:
        """delete.

        :param session:
        :type session: AsyncSession
        :rtype: None
        """
        await session.delete(self)
        await session.flush()
