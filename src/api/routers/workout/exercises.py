from fastapi import APIRouter, Depends

from schemas.workout.exercises import CreateExercise
from services.workout.exercise import ExercisesService

router = APIRouter(tags=["exercises"])


@router.get("/exercises")
def get_exercises():
    return {"message": "Hello World"}


@router.post("/exercise", status_code=201)
def create_exercise(
    exercise_data: CreateExercise,
    exercise_service: ExercisesService = Depends(ExercisesService),
):
    return exercise_service.create_exercise(exercise_data=exercise_data)
