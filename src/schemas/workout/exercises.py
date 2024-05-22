from fastapi import UploadFile
from pydantic import BaseModel

from schemas.images import ImagesSchema


class CreateExercise(BaseModel):
    name: str
    description: str
    video_url: str


class ExercisesSchema(CreateExercise):
    id: int
    image: ImagesSchema
