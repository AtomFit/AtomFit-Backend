from fastapi import Cookie

from schemas.users import UserSchema
from services.tokens import TokenDecoderService
from services.auth import AuthService
from services.users import UserService
from utils.unit_of_work import UnitOfWork, IUnitOfWork


def get_auth_service() -> AuthService:
    uow: IUnitOfWork = UnitOfWork()
    auth_service: AuthService = AuthService(uow)
    return auth_service


async def get_current_active_user(access: str = Cookie(None)) -> UserSchema:
    uow: IUnitOfWork = UnitOfWork()
    token_service: TokenDecoderService = TokenDecoderService(access, uow=uow)
    return await token_service.get_current_active_user()


def get_user_service() -> UserService:
    uow: IUnitOfWork = UnitOfWork()
    user_service: UserService = UserService(uow)
    return user_service
