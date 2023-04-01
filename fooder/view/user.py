from fastapi import APIRouter, Depends, Request
from ..model.user import User, CreateUserPayload
from ..controller.user import CreateUser


router = APIRouter(tags=["user"])


@router.post("", response_model=User)
async def create_user(
    request: Request,
    data: CreateUserPayload,
    contoller: CreateUser = Depends(CreateUser),
):
    return await contoller.call(data)
