from models.nutrition.user_goal_nutrients import UserGoalNutrientsOrm
from utils.repositories import SQLAlchemyRepository


class UserGoalNutrientsRepository(SQLAlchemyRepository):
    model = UserGoalNutrientsOrm
