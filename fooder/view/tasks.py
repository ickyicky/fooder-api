from fastapi import APIRouter, Depends, Request
from ..controller.tasks import CacheProductUsageData


router = APIRouter(prefix="/api", tags=["tasks"])


@router.post("/cache_product_usage_data")
async def create_user(
    request: Request,
    contoller: CacheProductUsageData = Depends(CacheProductUsageData),
):
    return await contoller.call()
