from fastapi import APIRouter, Depends
from starlette.responses import FileResponse

from utils.unit_of_work import UnitOfWork

router = APIRouter(tags=["images"])


@router.get("/image/{image_id}")
async def get_image(image_id: int, uow=UnitOfWork()):
    async with uow:
        image = await uow.images.find_one(filter={"id": image_id})
    return FileResponse(image.path)


@router.post("/image")
async def create_image(file: bytes, uow: UnitOfWork = Depends(UnitOfWork)) -> dict:
    async with uow:
        image_id = await uow.images.add_one(data=file)
        await uow.commit()
    return {"image_id": image_id[0]}
