from fastapi import HTTPException
from ..domain.product import Product as DBProduct
from .base import TasksSessionController


class CacheProductUsageData(TasksSessionController):
    async def call(self) -> None:
        async with self.async_session.begin() as session:
            try:
                await DBProduct.cache_usage_data(session)
                await session.commit()
            except Exception as e:
                raise HTTPException(status_code=400, detail=str(e))
