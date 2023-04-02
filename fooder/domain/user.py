from sqlalchemy.orm import Mapped
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from .base import Base, CommonMixin


class User(Base, CommonMixin):
    """Product."""

    username: Mapped[str]
    hashed_password: Mapped[str]

    def set_password(self, password) -> None:
        """set_password.

        :param password:
        :rtype: None
        """
        from ..auth import password_helper

        self.hashed_password = password_helper.hash(password)

    @classmethod
    async def get_by_username(
        cls, session: AsyncSession, username: str
    ) -> Optional["User"]:
        """get_by_username.

        :param session:
        :type session: AsyncSession
        :param username:
        :type username: str
        :rtype: Optional["User"]
        """
        query = select(cls).filter(cls.username == username)
        return await session.scalar(query.order_by(cls.id))

    @classmethod
    async def get(cls, session: AsyncSession, id: int) -> Optional["User"]:
        """get_by_username.

        :param session:
        :type session: AsyncSession
        :param id:
        :type id: int
        :rtype: Optional["User"]
        """
        query = select(cls).filter(cls.id == id)
        return await session.scalar(query.order_by(cls.id))

    @classmethod
    async def create(
        cls, session: AsyncSession, username: str, password: str
    ) -> "User":
        """create.

        :param session:
        :type session: AsyncSession
        :param username:
        :type username: str
        :param password:
        :type password: str
        :rtype: "User"
        """
        exsisting_user = await User.get_by_username(session, username)
        assert exsisting_user is None, "user already exists"
        user = cls(username=username)
        user.set_password(password)
        session.add(user)
        await session.flush()
        return user
