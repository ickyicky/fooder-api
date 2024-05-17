from fastapi import HTTPException
from fastapi.security import OAuth2PasswordRequestForm

from ..model.token import Token, RefreshTokenPayload
from ..domain.user import User as DBUser
from .base import BaseController
from ..auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    verify_refresh_token,
)


class CreateToken(BaseController):
    async def call(self, content: OAuth2PasswordRequestForm) -> Token:
        async with self.async_session.begin() as session:
            user = await authenticate_user(session, content.username, content.password)

            if user is None:
                raise HTTPException(
                    status_code=401, detail="Invalid username or password"
                )

            refresh_token = await create_refresh_token(session, user)
            access_token = create_access_token(user)

            return Token(
                access_token=access_token,
                refresh_token=refresh_token.token,
                token_type="bearer",
            )


class RefreshToken(BaseController):
    async def call(self, content: RefreshTokenPayload) -> Token:
        async with self.async_session.begin() as session:
            current_token = await verify_refresh_token(session, content.refresh_token)

            if current_token is None:
                raise HTTPException(status_code=401, detail="Invalid token")

            user = await DBUser.get(session, current_token.user_id)
            await current_token.delete(session)

            refresh_token = await create_refresh_token(session, user)
            access_token = create_access_token(user)

            return Token(
                access_token=access_token,
                refresh_token=refresh_token.token,
                token_type="bearer",
            )
