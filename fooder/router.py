from fastapi import APIRouter
from .view.product import router as product_router
from .view.diary import router as diary_router
from .view.meal import router as meal_router
from .view.entry import router as entry_router
from .view.token import router as token_router
from .view.user import router as user_router


router = APIRouter(prefix="/api")
router.include_router(product_router, prefix="/product", tags=["product"])
router.include_router(diary_router, prefix="/diary", tags=["diary"])
router.include_router(meal_router, prefix="/meal", tags=["meal"])
router.include_router(entry_router, prefix="/entry", tags=["entry"])
router.include_router(token_router, prefix="/token", tags=["token"])
router.include_router(user_router, prefix="/user", tags=["user"])
