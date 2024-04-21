from enum import Enum

from pydantic import BaseModel, Field, EmailStr

from schemas.nutrition.meal_nutrients import CreateMealNutrientsSchema


class LoginUserSchema(BaseModel):
    email: EmailStr
    password: str


class RegisterUserSchema(BaseModel):
    username: str
    email: EmailStr


class Goals(Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"


class UserMetricsSchema(BaseModel):
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    age: int = Field(..., gt=0)
    goal: Goals
    weight_preference: float = Field(..., gt=0)
    is_male: bool


class RegisterUserExtendSchema(RegisterUserSchema, UserMetricsSchema):
    password: str


class UpdateUser(BaseModel):
    is_active: bool
    is_superuser: bool


class UserSchema(RegisterUserSchema, UserMetricsSchema, UpdateUser):
    id: int

class UserExtendSchema(UserSchema):
    user_meal_goals: CreateMealNutrientsSchema

class UserUpdateSchema(UserMetricsSchema):
    username: str
