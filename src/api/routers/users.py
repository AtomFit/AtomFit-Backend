from fastapi import APIRouter, Depends

from api.dependencies import get_current_active_user
from schemas.users import UserSchema

router = APIRouter()


@router.get("/users/me", tags=["users"])
async def get_user(user: UserSchema = Depends(get_current_active_user)):
    return user