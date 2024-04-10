from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class UserSchema(BaseModel):
    id: int
    username: str
    email: str
    is_active: bool
    is_superuser: bool
    is_male: bool
    created_at: datetime
    class Config:
        orm_mode = True

class RegisterUserSchema(UserSchema):
    password: str
    created_at: Optional[datetime] = None