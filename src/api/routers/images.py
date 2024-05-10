from fastapi import APIRouter
from starlette.responses import FileResponse

from utils.unit_of_work import UnitOfWork

router = APIRouter(tags=["images"])

@router.get("/image/{image_id}")
async def get_image(image_id: int, uow=UnitOfWork()):
    async with uow:
        image = await uow.images.find_one(filter={"id": image_id})
    return FileResponse(image.path)
