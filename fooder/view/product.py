from fastapi import APIRouter, Depends, Request
from ..model.product import Product, CreateProductPayload, ListProductPayload
from ..controller.product import ListProduct, CreateProduct, GetProductByBarCode
from typing import Optional


router = APIRouter(tags=["product"])


@router.get("", response_model=ListProductPayload)
async def list_product(
    request: Request,
    controller: ListProduct = Depends(ListProduct),
    limit: int = 10,
    offset: int = 0,
    q: Optional[str] = None,
):
    return ListProductPayload(
        products=[p async for p in controller.call(limit=limit, offset=offset, q=q)]
    )


@router.post("", response_model=Product)
async def create_product(
    request: Request,
    data: CreateProductPayload,
    contoller: CreateProduct = Depends(CreateProduct),
):
    return await contoller.call(data)


@router.get("/by_barcode", response_model=Product)
async def get_by_bar_code(
    request: Request,
    barcode: str,
    contoller: GetProductByBarCode = Depends(GetProductByBarCode),
):
    return await contoller.call(barcode)
