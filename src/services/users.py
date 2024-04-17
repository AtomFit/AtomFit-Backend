from typing import Any

from exeptions.users import NoSuperUserException
from schemas.users import UserSchema, UserUpdateSchema, UpdateUser
from utils.unit_of_work import IUnitOfWork





class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(self, data: dict[str, Any]) -> UserSchema:
        async with self.uow:
            user = await self.uow.users.get_one(filter_by=data)  # type: ignore
        return user

    async def update_user(self, _id: str, data: UserUpdateSchema) -> int:
        data_dict = data.dict()
        data_dict["goal"] = data_dict["goal"].value
        async with self.uow:
            user_id = await self.uow.users.update_one(data=data_dict, _id=_id)  # type: ignore
            await self.uow.commit()
        return user_id

    async def delete_user(self, user_id: int, user: UserSchema) -> int:
        if not user.is_superuser and user_id != user.id:
            raise NoSuperUserException
        async with self.uow:
            deleted_user_id = await self.uow.users.delete_one(user_id)  # type: ignore
            await self.uow.commit()
        return deleted_user_id

    async def update_user_by_user_id(self, data: UpdateUser, user_id: int) -> int:
        data_dict = data.dict()
        async with self.uow:
            updated_user_id = await self.uow.users.update_one(data=data_dict, _id=user_id)  # type: ignore
            await self.uow.commit()
        return updated_user_id
