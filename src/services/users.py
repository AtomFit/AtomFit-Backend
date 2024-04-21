
from exeptions.users import NoSuperUserException
from schemas.users import UserSchema, UserUpdateSchema, UpdateUser, UserExtendSchema
from services.nutrition.user_nutrients_goal import UserGoalNutrientsService
from utils.unit_of_work import IUnitOfWork, UnitOfWork


class UserService:
    def __init__(self, current_user: UserSchema, uow: IUnitOfWork = UnitOfWork()):
        self.uow = uow
        self.current_user = current_user

    async def update_user(self, data: UserUpdateSchema) -> int:
        data_dict = data.dict()
        data_dict["goal"] = data_dict["goal"].value
        async with self.uow:
            user_id = await self.uow.users.update_one(data=data_dict, _id=self.current_user.id)     # type: ignore
            user = await self.uow.users.get_one(filter_by={"id": self.current_user.id})     # type: ignore
            user_goal_nutrients_service = UserGoalNutrientsService(user=user)
            current_user_new_goal = (
                user_goal_nutrients_service.create_obj_of_goal_nutrients()
            )
            await self.uow.user_goal_nutrients.update_one(      # type: ignore
                data=current_user_new_goal,
                _id=self.current_user.id,
                where_arg=(
                    self.uow.user_goal_nutrients.model.user_id == self.current_user.id  # type: ignore
                ),
            )
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
