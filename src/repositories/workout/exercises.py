from models.workout.exercise import ExerciseOrm
from utils.repositories import SQLAlchemyRepository


class ExercisesRepository(SQLAlchemyRepository):
    model = ExerciseOrm
