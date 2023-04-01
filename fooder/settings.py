from pydantic import BaseSettings
from typing import List


class Settings(BaseSettings):
    """Settings."""

    DB_URI: str
    ECHO_SQL: bool

    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    ALLOWED_ORIGINS: List[str] = ["*"]
