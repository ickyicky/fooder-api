import logging
from typing import AsyncIterator

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine

from .settings import Settings

log = logging.getLogger(__name__)
settings = Settings.parse_obj({})

if settings.DB_URI.startswith("sqlite"):
    settings.DB_URI = settings.DB_URI + "?check_same_thread=False"

"""
Asynchronous PostgreSQL database engine.
"""
async_engine = create_async_engine(
    settings.DB_URI,
    pool_pre_ping=True,
    echo=settings.ECHO_SQL,
    connect_args=(
        {"check_same_thread": False} if settings.DB_URI.startswith("sqlite") else {}
    ),
)
AsyncSessionLocal = async_sessionmaker(
    bind=async_engine,
    autocommit=False,
    autoflush=False,
    future=True,
)


async def get_session() -> AsyncIterator[async_sessionmaker]:
    try:
        yield AsyncSessionLocal
    except SQLAlchemyError as e:
        log.exception(e)
