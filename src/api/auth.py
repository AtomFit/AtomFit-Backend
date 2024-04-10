from fastapi import APIRouter

from api.dependencies import UowDep
from schemas.users import RegisterUserSchema

router = APIRouter()

@router.post("/register")
async def register(user: RegisterUserSchema, uow: UowDep):
    user_id = await uow.users.add_one(user, uow)
    return {"user_id": user_id}