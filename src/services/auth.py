from fastapi import Response


from exeptions.users import EmailAlreadyExistsException, UserNotFoundException
from schemas.tokens import TokenPairSchema
from schemas.users import (
    UserMetricsSchema,
    UserSchema,
    RegisterUserSchema,
    LoginUserSchema,
)
from services.tokens import TokenService
from services.users import UserService
from utils.unit_of_work import IUnitOfWork


class AuthService:
    ACCESS_TOKEN = "access"
    REFRESH_TOKEN = "refresh"

    async def register(self, user_data: RegisterUserSchema, uow: IUnitOfWork) -> int:
        user_data_dict = self.get_user_data_dict(user_data.user)
        user_metrics_data_dict = self.get_user_metrics_data_dict(user_data.user_metrics)

        user = await self.get_user(user_data_dict["email"], uow)
        if user:
            raise EmailAlreadyExistsException

        async with uow:
            user_id = await uow.users.add_one(data=user_data_dict)
            user_metrics_data_dict["user_id"] = user_id
            await uow.user_metrics.add_one(data=user_metrics_data_dict)
            await uow.commit()
        return user_id

    async def login(
        self, data: LoginUserSchema, uow: IUnitOfWork, response: Response
    ) -> dict:
        user = await self.get_user(data.email, uow)
        if user is None:
            raise UserNotFoundException

        token_service = TokenService(user)
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

    async def get_user(self, email: str, uow: IUnitOfWork):
        user_service = UserService()
        async with uow:
            user = await user_service.get_user(data={"email": email}, uow=uow)
        if user:
            return user

    def get_user_data_dict(self, user_data: UserSchema) -> dict:
        hashed_password = get_hashed_password(user_data.password)
        return {
            "email": user_data.email,
            "hashed_password": hashed_password,
            "username": user_data.username,
        }

    def get_user_metrics_data_dict(self, user_metrics_data: UserMetricsSchema) -> dict:
        return {
            "age": user_metrics_data.age,
            "height": user_metrics_data.height,
            "weight": user_metrics_data.weight,
            "goal": user_metrics_data.goal.value,
            "weight_preference": user_metrics_data.weight_preference,
            "is_male": user_metrics_data.is_male,
        }

    def get_hashed_password(password: str) -> str:
        return hash_password(password).decode("utf-8")
