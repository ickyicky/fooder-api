from fastapi import APIRouter, Depends, Request
from ..model.product import Product, CreateProductPayload, ListProductPayload
from ..controller.product import ListProduct, CreateProduct


router = APIRouter(tags=["product"])


@router.get("/", response_model=ListProductPayload)
async def list_product(
    request: Request,
    controller: ListProduct = Depends(ListProduct),
    limit: int = 10,
    offset: int = 0,
):
    return ListProductPayload(
        products=[p async for p in controller.call(limit=limit, offset=offset)]
    )


@router.post("/", response_model=Product)
async def create_product(
    request: Request,
    data: CreateProductPayload,
    contoller: CreateProduct = Depends(CreateProduct),
):
    return await contoller.call(data)
