from typing import AsyncIterator, Optional

from fastapi import HTTPException

from ..utils import product_finder
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
                    content.fiber,
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


class GetProductByBarCode(AuthorizedController):
    async def call(self, barcode: str) -> Product:
        async with self.async_session() as session:
            product = await DBProduct.get_by_barcode(session, barcode)

            if product:
                return Product.from_orm(product)

            try:
                product_data = product_finder.find(barcode)
            except product_finder.ProductNotFound:
                raise HTTPException(status_code=404, detail="Product not found")
            except product_finder.ParseError:
                raise HTTPException(
                    status_code=400, detail="Product was found, but unable to import"
                )

            try:
                product = await DBProduct.create(
                    session,
                    product_data.name,
                    product_data.carb,
                    product_data.protein,
                    product_data.fat,
                    product_data.fiber,
                    product_data.kcal,
                    barcode,
                )
                await session.commit()

                return Product.from_orm(await DBProduct.get_by_barcode(session, barcode))
            except AssertionError as e:
                raise HTTPException(status_code=400, detail=e.args[0])
