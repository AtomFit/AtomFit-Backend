from typing import Final, Any
import bcrypt
from fastapi import Response, Request

from exeptions.users import EmailAlreadyExistsException, UserNotFoundException
from schemas.users import (
    RegisterUserExtendSchema,
    LoginUserSchema,
    UserSchema,
)
from services.nutrition.user_nutrients_goal import UserGoalNutrientsService
from services.tokens import TokenEncoderService, TokenDecoderService
from utils.unit_of_work import IUnitOfWork


class AuthService:
    ACCESS_TOKEN: Final[str] = "access"
    REFRESH_TOKEN: Final[str] = "refresh"

    def __init__(self, uow: IUnitOfWork) -> None:
        self.uow = uow

    async def register(self, user_data: RegisterUserExtendSchema) -> UserSchema | None:
        user_data_dict = self.get_user_data_dict(user_data)

        async with self.uow:
            user = await self.uow.users.get_one(    # type: ignore
                filter_by={"email": user_data_dict["email"]}
            )
            if user:
                raise EmailAlreadyExistsException
            user_id = await self.uow.users.add_one(data=user_data_dict)  # type: ignore
            user = await self.uow.users.get_one(filter_by={"id": user_id})  # type: ignore
            user_goal_nutrients_service = UserGoalNutrientsService(user=user)
            user_new_goal = user_goal_nutrients_service.create_obj_of_goal_nutrients()
            await self.uow.user_goal_nutrients.add_one(data=user_new_goal)  # type: ignore
            await self.uow.commit()
        return user

    async def login(self, data: LoginUserSchema, response: Response) -> dict[str, str]:
        async with self.uow:
            user = await self.uow.users.get_one(filter_by={"email": data.email})    # type: ignore
        if user is None:
            raise UserNotFoundException

        token_service = TokenEncoderService(user)
        access_token = token_service.create_access_token()
        refresh_token = token_service.create_refresh_token()
        response.set_cookie(
            key=self.REFRESH_TOKEN,
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="strict",
        )
        response.set_cookie(
            key=self.ACCESS_TOKEN,
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
        )
        return {"result": "success"}

    def logout(self, response: Response) -> None:
        response.delete_cookie(key=self.ACCESS_TOKEN)
        response.delete_cookie(key=self.REFRESH_TOKEN)

    async def refresh(self, response: Response, request: Request) -> None:
        refresh_token: str | None = request.cookies.get(self.REFRESH_TOKEN)
        token_decode_service = TokenDecoderService(refresh_token, uow=self.uow)
        user = await token_decode_service.get_current_active_user()

        token_encode_service = TokenEncoderService(user)
        access_token = token_encode_service.create_access_token()
        response.set_cookie(
            key=self.ACCESS_TOKEN,
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
        )

    def get_user_data_dict(self, user_data: RegisterUserExtendSchema) -> dict[str, Any]:
        hashed_password = self.hash_password(user_data.password)
        return {
            "email": user_data.email,
            "hashed_password": hashed_password,
            "username": user_data.username,
            "age": user_data.age,
            "height": user_data.height,
            "weight": user_data.weight,
            "goal": user_data.goal.value,
            "weight_preference": user_data.weight_preference,
            "is_male": user_data.is_male,
        }

    @staticmethod
    def hash_password(password: str) -> str:
        salt = bcrypt.gensalt()
        pwd_bytes: bytes = password.encode()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode("utf-8")
