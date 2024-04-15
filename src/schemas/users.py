from enum import Enum

from pydantic import BaseModel, Field, EmailStr


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


class UserSchema(RegisterUserSchema, UserMetricsSchema):
    id: int
    is_active: bool
    is_superuser: bool
    class Config:
        orm_mode = True
