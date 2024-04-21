from models.nutrition.meal_nutrients import MealNutrientsOrm
from utils.repositories import SQLAlchemyRepository


class MealNutrientsRepository(SQLAlchemyRepository):
    model = MealNutrientsOrm
