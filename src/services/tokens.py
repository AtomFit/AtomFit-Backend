from datetime import timedelta, datetime, timezone
from typing import Final, Any
import jwt
from fastapi import HTTPException, status
from jwt import InvalidTokenError

from config import settings
from exeptions.users import InactiveUserException
from schemas.users import UserSchema
from utils.unit_of_work import IUnitOfWork


class TokenEncoderService:
    ACCESS_TOKEN: Final[str] = "access"
    REFRESH_TOKEN: Final[str] = "refresh"
    TOKEN_TYPE_FIELD: Final[str] = "token_type"

    jwt_payload: dict[Any, Any] = {}
    expire_timedelta: timedelta | None = None
    private_key = settings.auth_jwt.private_key
    algorithm: str = settings.auth_jwt.algorithm
    expire_minutes: int = settings.auth_jwt.access_token_expire_minutes

    def __init__(self, user: UserSchema):
        self.user = user

    def create_access_token(self) -> str:
        self.jwt_payload = {
            self.TOKEN_TYPE_FIELD: self.ACCESS_TOKEN,
            "sub": self.user.email,
            "username": self.user.username,
            "email": self.user.email,
            # "logged_in_at": now,
        }
        return self.encode_jwt()

    def create_refresh_token(self) -> str:
        self.jwt_payload = {
            self.TOKEN_TYPE_FIELD: self.REFRESH_TOKEN,
            "sub": self.user.email,
            # "username": user.username,
        }
        self.expire_timedelta = timedelta(
            days=settings.auth_jwt.refresh_token_expire_days
        )
        return self.encode_jwt()

    def encode_jwt(self) -> str:
        to_encode = self.jwt_payload.copy()
        now = datetime.now(timezone.utc)
        if self.expire_timedelta:
            expire = now + self.expire_timedelta
        else:
            expire = now + timedelta(minutes=self.expire_minutes)
        to_encode.update(
            exp=(expire.timestamp()),
            iat=(now.timestamp()),
        )
        encoded = jwt.encode(
            to_encode,
            self.private_key,   # type: ignore
            algorithm=self.algorithm,
        )
        return encoded


class TokenDecoderService:
    public_key: str = settings.auth_jwt.public_key  # type: ignore
    algorithm: str = settings.auth_jwt.algorithm

    user: UserSchema | None = None

    def __init__(self, token: str | None, uow: IUnitOfWork):
        self.token = token
        self.uow = uow

    def decode_jwt(self) -> dict[Any, Any]:
        decoded: dict[Any, Any] = jwt.decode(
            self.token,  # type: ignore
            self.public_key,
            algorithms=[self.algorithm],
        )
        return decoded

    def get_current_token_payload(self) -> dict[str, str]:
        try:
            payload = self.decode_jwt()
        except InvalidTokenError as e:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail=f"invalid token error: {e}",
            )
        return payload

    async def get_current_active_user(self) -> UserSchema:
        payload = self.get_current_token_payload()
        email: str | None = payload.get("sub")
        async with self.uow:
            self.user = await self.uow.users.get_one(filter_by={"email": email})    # type: ignore

        if self.user is None:
            raise InvalidTokenError

        if self.user.is_active is False:
            raise InactiveUserException
        return self.user
