from fastapi import UploadFile
from pydantic import BaseModel

from schemas.images import ImagesSchema


class CreateExercise(BaseModel):
    name: str
    description: str
    video_url: str
    image: UploadFile

class ExercisesSchema(CreateExercise):
    id: int
    image: ImagesSchema
