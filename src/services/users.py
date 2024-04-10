
from schemas.users import UserSchemaWithPass, UserMetricsSchema
from utils.unit_of_work import IUnitOfWork


class UsersService:
    async def add_user(self, user_data: UserSchemaWithPass, user_metrics_data: UserMetricsSchema,
                       uow: IUnitOfWork) -> int:
        user_data_dict = user_data.model_dump()
        user_metrics_data_dict = user_metrics_data.model_dump()
        async with uow:
            user_id = await uow.users.add_one(data=user_data_dict)
            user_metrics_data_dict['user_id'] = user_id
            await uow.user_metrics.add_one(data=user_metrics_data_dict)
            await uow.commit()
        return user_id

    async def get_user(self, data: dict, uow: IUnitOfWork) -> dict:
        async with uow:
            user = await uow.users.find_one(filter_by=data)
        return user
