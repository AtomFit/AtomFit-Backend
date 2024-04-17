from fastapi import APIRouter, Depends

from api.dependencies import (
    get_current_active_user,
    get_user_service,
    get_current_super_user,
)
from schemas.users import UserSchema, UserUpdateSchema, UpdateUser

router = APIRouter()


@router.get("/users/me", tags=["users"], response_model=UserSchema)
async def get_user(user: UserSchema = Depends(get_current_active_user)) -> UserSchema:
    return user


@router.patch("/users/me", tags=["users"], response_model=dict)
async def update_user(
    data: UserUpdateSchema,
    user: UserSchema = Depends(get_current_active_user),
    user_service=Depends(get_user_service),
) -> dict[str, int]:
    user_id: int = await user_service.update_user(_id=user.id, data=data)
    print(user_id)
    return {"user_id": user_id}


@router.put("/user/{user_id}", tags=["users"], response_model=dict)
async def update_user_by_user_id(
    user_id: int,
    data: UpdateUser = Depends(),
    user_service=Depends(get_user_service),
    user=Depends(get_current_super_user),
) -> dict[str, int]:
    user_id: int = await user_service.update_user_by_user_id(data=data, user_id=user_id)
    return {"user_id": user_id}
