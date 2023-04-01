from fastapi import APIRouter, Depends, Request
from ..model.token import Token
from ..controller.token import CreateToken
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated


router = APIRouter(tags=["token"])


@router.post("/", response_model=Token)
async def create_token(
    request: Request,
    data: Annotated[OAuth2PasswordRequestForm, Depends()],
    controller: CreateToken = Depends(CreateToken),
):
    return await controller.call(data)
