from datetime import datetime, timezone
from sqlalchemy import text, func, and_

from schemas.nutrition.meal_nutrients import (
    MealNutrientsSchema,
    CreateMealNutrientsSchema,
    MealNutrientsForDay,
)
from schemas.users import UserSchema
from utils.unit_of_work import UnitOfWork, IUnitOfWork


class MealNutrientsService:

    def __init__(
        self,
        user: UserSchema,
        uow: IUnitOfWork = UnitOfWork(),
    ):
        self.user_goal_nutrients: dict = {}
        self.uow = uow
        self.user = user

    async def get_meal_nutrients_by_id(self, meal_nutrients_id: int) -> MealNutrientsSchema:
        async with self.uow:
            meal_nutrients = await self.uow.meal_nutrients.get_one(  # type: ignore
                filter_by={"id": meal_nutrients_id},
            )
        result_dto = MealNutrientsSchema.model_validate(meal_nutrients, from_attributes=True)
        return result_dto

    async def get_all_meal_nutrients(self) -> list[MealNutrientsSchema] | None:
        async with self.uow:
            meal_nutrients = await self.uow.meal_nutrients.get_all(  # type: ignore
                filter_by={"user_id": self.user.id},
                order_by=text("log_date DESC"),
            )
        if not meal_nutrients:
            return None
        result_dto = [
            MealNutrientsSchema.model_validate(meal, from_attributes=True)
            for meal in meal_nutrients
        ]

        return result_dto

    async def log_meal_nutrients(
        self,
        meal_nutrients: CreateMealNutrientsSchema,
    ) -> int:
        meal_nutrients_dict = meal_nutrients.dict()
        meal_nutrients_dict["user_id"] = self.user.id
        async with self.uow:
            meal_nutrients_id = await self.uow.meal_nutrients.add_one(  # type: ignore
                data=meal_nutrients_dict
            )
            await self.uow.commit()
        return meal_nutrients_id

    async def get_meal_nutrients_sum(
        self, for_date: datetime = datetime.now(timezone.utc)
    ) -> MealNutrientsForDay:
        async with self.uow:
            model = self.uow.meal_nutrients.model  # type: ignore
            meal_nutrients = await self.uow.meal_nutrients.get_all(  # type: ignore
                select_by=[
                    func.sum(model.carbohydrates).label("carbohydrates"),
                    func.sum(model.proteins).label("proteins"),
                    func.sum(model.fats).label("fats"),
                    func.sum(model.calories).label("calories"),
                    func.sum(model.fibers).label("fibers"),
                    func.sum(model.sugars).label("sugars"),
                    func.date(model.log_date).label("log_date"),
                ],
                where=and_(
                    model.user_id == self.user.id,
                    func.date(model.log_date) == for_date.date(),
                ),
                group_by=[func.date(model.log_date)],
                order_by=text("DATE(log_date) DESC"),
            )
        if meal_nutrients:
            result_dto = MealNutrientsForDay.model_validate(
                meal_nutrients,
                from_attributes=True,
            )
            return result_dto
        else:
            return MealNutrientsForDay()

    async def update_meal_nutrients(
        self, meal_nutrients_id: int, meal_nutrients: CreateMealNutrientsSchema
    ) -> MealNutrientsSchema:
        meal_nutrients_dict = meal_nutrients.dict()
        async with self.uow:
            await self.uow.meal_nutrients.update_one(  # type: ignore
                _id=meal_nutrients_id,
                data=meal_nutrients_dict,
            )
            await self.uow.commit()
        return await self.get_meal_nutrients_by_id(meal_nutrients_id)

    async def delete_meal_nutrients(self, meal_nutrients_id: int):
        async with self.uow:
            await self.uow.meal_nutrients.delete_one(  # type: ignore
                _id=meal_nutrients_id
            )
            await self.uow.commit()

    async def get_user_goal_nutrients(self):
        async with self.uow:
            user_goal_nutrients = await self.uow.user_goal_nutrients.get_one(
                filter_by={"user_id": self.user.id}
            )
        return user_goal_nutrients
