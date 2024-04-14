from fastapi import Cookie

from schemas.users import UserSchema
from services.tokens import TokenDecoderService
from services.auth import AuthService
from utils.unit_of_work import UnitOfWork


def get_auth_service() -> AuthService:
    uow = UnitOfWork()
    auth_service = AuthService(uow)
    return auth_service


async def get_current_active_user(access: str = Cookie(None)) -> UserSchema:
    uow = UnitOfWork()
    token_service = TokenDecoderService(access, uow=uow)
    return await token_service.get_current_active_user()
