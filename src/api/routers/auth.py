from typing import Annotated
from fastapi import APIRouter, Depends, Response, Request

from api.dependencies import get_auth_service
from schemas.users import LoginUserSchema, RegisterUserExtendSchema, UserSchema
from services.auth import AuthService


router = APIRouter()


@router.post("/register", tags=["auth"])
async def register(
    user_data: RegisterUserExtendSchema,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> UserSchema | None:
    return await auth_service.register(user_data=user_data)


@router.post("/login", tags=["auth"], response_model=dict)
async def login(
    user_data: LoginUserSchema,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, str]:
    token_pair = await auth_service.login(data=user_data, response=response)
    return token_pair


@router.post("/logout", tags=["auth"])
async def logout(
    response: Response, auth_service: Annotated[AuthService, Depends(get_auth_service)]
) -> dict[str, str]:
    auth_service.logout(response=response)
    return {"result": "success"}


@router.post("/refresh", tags=["auth"])
async def refresh(
    request: Request,
    response: Response,
    auth_service: Annotated[AuthService, Depends(get_auth_service)],
) -> dict[str, str]:
    await auth_service.refresh(response=response, request=request)
    return {"result": "success"}
