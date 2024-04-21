
from schemas.users import UserSchema, Goals


class UserGoalNutrientsService:
    def __init__(self, user: UserSchema):
        self.user = user
        self.user_goal_nutrients: dict = {}

    def calculate_bmr(self) -> float:
        if self.user.is_male:
            return (
                66
                + (6.23 * self.user.weight)
                + (12.7 * self.user.height)
                - (6.8 * self.user.age)
            )
        else:
            return (
                655
                + (4.35 * self.user.weight)
                + (4.7 * self.user.height)
                - (4.7 * self.user.age)
            )

    @staticmethod
    def adjust_bmr_for_activity(bmr: float, activity_factor: float) -> float:
        return bmr * activity_factor

    def adjust_bmr_for_goal(self, bmr: float):
        if self.user.goal == Goals.lose:
            return bmr - 500
        elif self.user.goal == Goals.gain:
            return bmr + 500
        return bmr

    @staticmethod
    def calculate_macros(bmr: float) -> dict:
        protein_ratio = 0.25
        fat_ratio = 0.25
        carb_ratio = 0.5

        protein_calories = protein_ratio * bmr
        fat_calories = fat_ratio * bmr
        carb_calories = carb_ratio * bmr

        protein_grams = protein_calories / 4
        fat_grams = fat_calories / 9
        carb_grams = carb_calories / 4

        return {
            "proteins": protein_grams,
            "fats": fat_grams,
            "carbohydrates": carb_grams,
        }

    @staticmethod
    def calculate_additional_metrics(bmr: float) -> dict:
        calories = bmr
        fibers = (calories / 1000)*14  # 14 grams of fiber per 1000 calories
        sugars = (
            0.1 * (calories * 0.5) / 4
        )  # Assuming 10% of carbohydrate calories are from sugar
        return {"calories": calories, "fibers": fibers, "sugars": sugars}

    def create_obj_of_goal_nutrients(self) -> dict:

        bmr = self.calculate_bmr()
        bmr = self.adjust_bmr_for_goal(bmr)

        activity_factor = 1  # Modify as needed for different activity levels
        bmr = self.adjust_bmr_for_activity(bmr, activity_factor)

        macros = self.calculate_macros(bmr)
        additional_metrics = self.calculate_additional_metrics(bmr)

        self.user_goal_nutrients = {
            "user_id": self.user.id,
            **macros,
            **additional_metrics,
        }
        return self.user_goal_nutrients
