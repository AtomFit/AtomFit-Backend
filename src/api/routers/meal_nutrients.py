from datetime import datetime, timezone
from typing import Optional
from fastapi import APIRouter, Depends

from api.dependencies import (
    get_meal_nutrients_service,
)
from schemas.nutrition.meal_nutrients import (
    MealNutrientsSchema,
    CreateMealNutrientsSchema,
    MealNutrientsForDay,
)
from services.nutrition.meal_nutirents import MealNutrientsService

router = APIRouter()


@router.post(
    "/meal_nutrients",
    tags=["meal_nutrients"],
    response_model=dict[str, int],
    status_code=201,
    description="Log nutrients of a meal, the meal nutrients id will be returned",
)
async def log_meal(
    meal_nutrients: CreateMealNutrientsSchema,
    meal_nutrients_service: MealNutrientsService = Depends(get_meal_nutrients_service),
) -> dict[str, int]:
    meal_nutrients_id = await meal_nutrients_service.log_meal_nutrients(
        meal_nutrients=meal_nutrients,
    )
    return {"meal_nutrients_id": meal_nutrients_id}


@router.get(
    "/meals_nutrients",
    tags=["meal_nutrients"],
    response_model=list[MealNutrientsSchema] | None,
    description="Get all meal nutrients history",
)
async def get_meal_nutrients_history(
    meal_nutrients_service: MealNutrientsService = Depends(get_meal_nutrients_service),
) -> list[MealNutrientsSchema] | None:
    return await meal_nutrients_service.get_all_meal_nutrients()


@router.get(
    "/meals_nutrients/progress/",
    tags=["meal_nutrients"],
    response_model=MealNutrientsForDay,
    description="Get progress for a specific day, if date is not provided, it will default to today",
)
async def get_progress_by_day(
    for_date: Optional[datetime] = datetime.now(timezone.utc),
    meal_nutrients_service=Depends(get_meal_nutrients_service),
) -> MealNutrientsForDay:
    return await meal_nutrients_service.get_meal_nutrients_sum(for_date=for_date)


@router.patch(
    "/meal_nutrients/{meal_nutrients_id}",
    tags=["meal_nutrients"],
    response_model=MealNutrientsSchema,
    description="Update meal nutrients, returns the updated meal nutrients",
)
async def update_meal_nutrients(
    meal_nutrients_id: int,
    meal_nutrients: CreateMealNutrientsSchema,
    meal_nutrients_service: MealNutrientsService = Depends(get_meal_nutrients_service),
) -> MealNutrientsSchema:
    return await meal_nutrients_service.update_meal_nutrients(
        meal_nutrients_id=meal_nutrients_id,
        meal_nutrients=meal_nutrients,
    )


@router.delete("/meal_nutrients/{meal_nutrients_id}", tags=["meal_nutrients"], response_model=dict)
async def delete_meal_nutrients(
    meal_nutrients_id: int,
    meal_nutrients_service: MealNutrientsService = Depends(get_meal_nutrients_service),
) -> dict[str, int]:
    deleted_meal_nutrients_id: int = await meal_nutrients_service.delete_meal_nutrients(
        meal_nutrients_id=meal_nutrients_id,
    )
    return {"meal_nutrients_id": deleted_meal_nutrients_id}


@router.get(
    "/user_goal_nutrients", tags=["meal_nutrients"], response_model=CreateMealNutrientsSchema
)
async def get_user_goal_nutrients(
    meal_nutrients_service: MealNutrientsService = Depends(get_meal_nutrients_service),
) -> CreateMealNutrientsSchema:
    return await meal_nutrients_service.get_user_goal_nutrients()
