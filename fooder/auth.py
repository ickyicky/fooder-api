from passlib.context import CryptContext
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker
from jose import JWTError, jwt
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, FastAPI, HTTPException
from fastapi_users.password import PasswordHelper
from sqlalchemy.ext.asyncio import async_sessionmaker
from typing import AsyncGenerator, Dict, Annotated, Optional
from datetime import datetime, timedelta
from .settings import Settings
from .domain.user import User
from .domain.token import RefreshToken
from .db import get_session


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/token")
settings = Settings()
password_helper = PasswordHelper(pwd_context)

AsyncSessionDependency = Annotated[async_sessionmaker, Depends(get_session)]
TokenDependency = Annotated[str, Depends(oauth2_scheme)]


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


async def authenticate_user(
    session: AsyncSession, username: str, password: str
) -> AsyncGenerator[User, None]:
    user = await User.get_by_username(session, username)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user


async def verify_refresh_token(
    session: AsyncSession, token: str
) -> AsyncGenerator[User, None]:
    try:
        payload = jwt.decode(
            token, settings.REFRESH_SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        username: str = payload.get("sub")
        if username is None:
            return
    except JWTError:
        return

    user = await User.get_by_username(session, username)
    current_token = await RefreshToken.get_token(session, user.id)
    if current_token is not None and current_token.token == token:
        return user


def create_access_token(user: User) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {
        "sub": user.username,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


async def create_refresh_token(session: AsyncSession, user: User) -> RefreshToken:
    expire = datetime.utcnow() + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    to_encode = {
        "sub": user.username,
        "exp": expire,
    }
    encoded_jwt = jwt.encode(
        to_encode, settings.REFRESH_SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return await RefreshToken.create(session, token=encoded_jwt, user_id=user.id)


async def get_current_user(
    session: AsyncSessionDependency, token: TokenDependency
) -> User:
    async with session() as session:
        try:
            payload = jwt.decode(
                token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
            )
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401, detail="Unathorized")
        except JWTError:
            raise HTTPException(status_code=401, detail="Unathorized")

        return await User.get_by_username(session, username)
