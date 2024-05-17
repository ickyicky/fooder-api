from typing import Annotated, Any
from fastapi import Depends
from sqlalchemy.ext.asyncio import async_sessionmaker
from ..db import get_session
from ..auth import get_current_user
from ..domain.user import User


AsyncSession = Annotated[async_sessionmaker, Depends(get_session)]
UserDependency = Annotated[User, Depends(get_current_user)]


class BaseController:
    def __init__(self, session: AsyncSession) -> None:
        self.async_session = session

    async def call(self, *args, **kwargs) -> Any:
        raise NotImplementedError

    async def __call__(self, *args, **kwargs) -> Any:
        return await self.call(*args, **kwargs)


class AuthorizedController(BaseController):
    def __init__(self, session: AsyncSession, user: UserDependency) -> None:
        super().__init__(session)
        self.user = user
