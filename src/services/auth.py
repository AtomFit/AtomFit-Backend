from typing import Final
import bcrypt
from fastapi import Response, Request

from exeptions.users import EmailAlreadyExistsException, UserNotFoundException
from schemas.users import (
    UserSchema,
    RegisterUserSchema,
    LoginUserSchema,
)
from services.tokens import TokenEncoderService, TokenDecoderService
from services.users import UserService
from utils.unit_of_work import IUnitOfWork


class AuthService:
    ACCESS_TOKEN: Final[str] = "access"
    REFRESH_TOKEN: Final[str] = "refresh"

    def __init__(self, uow: IUnitOfWork):
        self.uow = uow
        self.user_service = UserService(uow=self.uow)

    async def register(self, user_data: RegisterUserSchema) -> int:
        user_data_dict = self.get_user_data_dict(user_data)
        user = await self.get_user(user_data_dict["email"])
        if user:
            raise EmailAlreadyExistsException

        async with self.uow:
            user_id = await self.uow.users.add_one(data=user_data_dict)
            await self.uow.commit()
        return user_id

    async def login(self, data: LoginUserSchema, response: Response) -> dict:
        user = await self.get_user(data.email)
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

    def logout(self, response: Response):
        response.delete_cookie(key=self.ACCESS_TOKEN)
        response.delete_cookie(key=self.REFRESH_TOKEN)

    async def refresh(self, response: Response, request: Request):
        refresh_token = request.cookies.get(self.REFRESH_TOKEN)
        token_service = TokenDecoderService(refresh_token, uow=self.uow)
        user = await token_service.get_current_active_user()

        token_service = TokenEncoderService(user)
        access_token = token_service.create_access_token()
        response.set_cookie(
            key=self.ACCESS_TOKEN,
            value=access_token,
            httponly=True,
            secure=True,
            samesite="strict",
        )

    async def get_user(self, email: str):
        user_service = UserService(uow=self.uow)
        async with self.uow:
            user = await user_service.get_user(data={"email": email})
        if user:
            return user

    def get_user_data_dict(self, user_data: UserSchema) -> dict:
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
