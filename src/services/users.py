
from schemas.users import UserSchema
from utils.unit_of_work import IUnitOfWork


class UserService:
    def __init__(self, uow: IUnitOfWork):
        self.uow = uow

    async def get_user(self, data: dict,) -> UserSchema:
        async with self.uow:
            user = await self.uow.users.get_one(filter_by=data)
        return user
