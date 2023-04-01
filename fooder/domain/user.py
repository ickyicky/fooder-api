from sqlalchemy.orm import Mapped
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .base import Base, CommonMixin


class User(Base, CommonMixin):
    """Product."""

    username: Mapped[str]
    hashed_password: Mapped[str]

    @classmethod
    async def get_by_username(
        cls, session: AsyncSession, username: str
    ) -> Optional["User"]:
        query = select(cls).filter(cls.username == username)
        return await session.scalar(query.order_by(cls.id))

    def set_password(self, password) -> None:
        from ..auth import password_helper

        self.hashed_password = password_helper.hash(password)

    @classmethod
    async def create(
        cls, session: AsyncSession, username: str, password: str
    ) -> "User":
        exsisting_user = await User.get_by_username(session, username)
        assert exsisting_user is None, "user already exists"
        user = cls(username=username)
        user.set_password(password)
        session.add(user)
        await session.flush()
        return user
