from fastapi import Cookie, Depends

from exeptions.users import NoSuperUserException
from schemas.users import UserSchema
from services.nutrition.meal_nutirents import MealNutrientsService
from services.nutrition.user_nutrients_goal import UserGoalNutrientsService
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


async def get_current_super_user(access: str = Cookie(None)) -> UserSchema:
    uow: IUnitOfWork = UnitOfWork()
    token_service: TokenDecoderService = TokenDecoderService(access, uow=uow)
    res = await token_service.get_current_active_user()
    if not res.is_superuser:
        raise NoSuperUserException
    return res


def get_user_service(current_user: UserSchema = Depends(get_current_active_user)) -> UserService:
    user_service: UserService = UserService(current_user)
    return user_service


def get_user_goal_nutrients_service(
    current_user: UserSchema = Depends(get_current_active_user),
) -> UserGoalNutrientsService:
    user_goal_nutrients_service: UserGoalNutrientsService = UserGoalNutrientsService(
        user=current_user
    )
    return user_goal_nutrients_service


def get_meal_nutrients_service(
    user: UserSchema = Depends(get_current_active_user),
) -> MealNutrientsService:
    meal_nutrients_service: MealNutrientsService = MealNutrientsService(user=user)
    return meal_nutrients_service
