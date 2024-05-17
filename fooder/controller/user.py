from fastapi import HTTPException

from ..model.user import User, CreateUserPayload
from ..domain.user import User as DBUser
from .base import BaseController


class CreateUser(BaseController):
    async def call(self, content: CreateUserPayload) -> User:
        async with self.async_session.begin() as session:
            try:
                user = await DBUser.create(
                    session,
                    content.username,
                    content.password,
                )
                return User.from_orm(user)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])
