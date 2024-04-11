from typing import Annotated
from fastapi import APIRouter, Depends, Response

from schemas.users import RegisterUserSchema, LoginUserSchema
from services.auth import AuthService
from utils.unit_of_work import IUnitOfWork, UnitOfWork

router = APIRouter()


@router.post("/register", tags=["auth"])
async def register(user_data: RegisterUserSchema, uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
                   auth_service: Annotated[AuthService, Depends(AuthService)]):
    user_id = await auth_service.register(user_data=user_data, uow=uow)
    return {"user_id": user_id}


@router.post("/login", tags=["auth"], response_model=dict)
async def login(user_data: LoginUserSchema, response: Response, uow: Annotated[IUnitOfWork, Depends(UnitOfWork)],
                auth_service: Annotated[AuthService, Depends(AuthService)]):
    token_pair = await auth_service.login(data=user_data, uow=uow, response=response)
    return token_pair


@router.post("/logout", tags=["auth"])
async def logout(response: Response):
    response.delete_cookie(key=AuthService.ACCESS_TOKEN)
    response.delete_cookie(key=AuthService.REFRESH_TOKEN)
    return {"result": "success"}
