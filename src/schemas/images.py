from pydantic import BaseModel


class ImagesSchema(BaseModel):
    id: int
    path: str
