from enum import Enum

from pydantic import BaseModel, Field, EmailStr


class UserSchema(BaseModel):
    id: int
    username: str
    email: EmailStr
    password: str
    class Config:
        orm_mode = True


class Goals(Enum):
    lose = "lose"
    maintain = "maintain"
    gain = "gain"


class UserMetricsSchema(BaseModel):
    height: float = Field(..., gt=0)
    weight: float = Field(..., gt=0)
    age: int = Field(..., gt=0)
    goal: str = Field(..., enum=Goals)
    weight_preference: float = Field(..., gt=0)
    is_male: bool


class RegisterUserSchema(BaseModel):
    user_metrics: UserMetricsSchema
    user: UserSchema
