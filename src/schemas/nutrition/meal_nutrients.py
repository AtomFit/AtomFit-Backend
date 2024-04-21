from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CreateMealNutrientsSchema(BaseModel):
    proteins: int = 0
    fats: int = 0
    carbohydrates: int = 0
    calories: int = 0
    fibers: int = 0
    sugars: int = 0


class MealNutrientsForDay(CreateMealNutrientsSchema):
    id: int = 0
    log_date: Optional[datetime] = datetime.now()


class MealNutrientsSchema(CreateMealNutrientsSchema):
    id: int
    user_id: int
    log_date: datetime
