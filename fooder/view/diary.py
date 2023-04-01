from fastapi import APIRouter, Depends, Request
from ..model.diary import Diary
from ..controller.diary import GetDiary
from datetime import date


router = APIRouter(tags=["diary"])


@router.get("", response_model=Diary)
async def get_diary(
    request: Request,
    date: date,
    controller: GetDiary = Depends(GetDiary),
):
    return await controller.call(date)
