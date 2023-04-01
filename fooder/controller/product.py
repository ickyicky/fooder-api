from typing import AsyncIterator, Optional

from fastapi import HTTPException

from ..model.product import Product, CreateProductPayload
from ..domain.product import Product as DBProduct
from .base import AuthorizedController


class CreateProduct(AuthorizedController):
    async def call(self, content: CreateProductPayload) -> Product:
        async with self.async_session.begin() as session:
            try:
                product = await DBProduct.create(
                    session,
                    content.name,
                    content.carb,
                    content.protein,
                    content.fat,
                )
                return Product.from_orm(product)
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])


class ListProduct(AuthorizedController):
    async def call(
        self, limit: int, offset: int, q: Optional[str]
    ) -> AsyncIterator[Product]:
        async with self.async_session() as session:
            async for product in DBProduct.list_all(
                session, limit=limit, offset=offset, q=q
            ):
                yield Product.from_orm(product)
