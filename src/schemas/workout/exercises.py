from pydantic import BaseModel
import enum
from schemas.images import ImagesSchema


class MuscleGroups(enum.Enum):
    traps = "traps"
    lats = "lats"
    lower_back = "lower_back"
    romboids = "romboids"

    abs = "abs"

    biceps = "biceps"
    triceps = "triceps"
    forearms = "forearms"

    neck = "neck"

    chest = "chest"

    shoulders = "shoulders"

    glutes = "glutes"
    quads = "quads"
    hamstrings = "hamstrings"
    calves = "calves"


class CreateExercise(BaseModel):
    name: str
    description: str
    video_url: str
    muscles: list[MuscleGroups]


class ExercisesSchema(CreateExercise):
    id: int
    image: ImagesSchema
