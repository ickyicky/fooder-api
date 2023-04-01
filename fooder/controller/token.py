from typing import AsyncIterator, Annotated

from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordRequestForm

from ..model.token import Token
from ..domain.user import User as DBUser
from .base import BaseController, AsyncSession
from ..auth import authenticate_user, create_access_token


class CreateToken(BaseController):
    async def call(self, content: OAuth2PasswordRequestForm) -> Token:
        async with self.async_session() as session:
            user = await authenticate_user(session, content.username, content.password)

            if user is None:
                raise HTTPException(
                    status_code=401, detail="Invalid username or password"
                )

            access_token = create_access_token(user)

            return Token(
                access_token=access_token,
                token_type="bearer",
            )
