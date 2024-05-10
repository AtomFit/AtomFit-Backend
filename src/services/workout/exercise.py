from schemas.workout.exercises import CreateExercise
from utils.unit_of_work import UnitOfWork


class ExercisesService:

    def __init__(self):
        self.uow = UnitOfWork()

    async def get_exercises(self) -> list:
        async with self.uow:
            exercises = await self.uow.exercises.find_all()
            if not exercises:
                return []
            exercises_list = [exercise.to_dict() for exercise in exercises]
        return exercises_list

    async def get_exercise(self, exercise_id: int) -> dict:
        async with self.uow:
            exercise = await self.uow.exercises.find_one(filter={"id": exercise_id})
            if not exercise:
                return {}
            exercise_dict = exercise.to_dict()
        return exercise_dict

    async def create_exercise(self, exercise_data: CreateExercise) -> int:
        async with self.uow:
            image_id = await self.uow.images.add_one(data=exercise_data.image.file)
            exercise_dict = self.exercise_to_dict(exercise_data, image_id)
            exercise_id = await self.uow.exercises.add_one(data=exercise_dict)
            await self.uow.commit()
        return exercise_id[0]

    async def delete_exercise(self, exercise_id: int) -> None:
        async with self.uow:
            await self.uow.exercises.delete_one(_id=exercise_id)
            await self.uow.commit()

    @staticmethod
    def exercise_to_dict(exercise, image_id: int):
        return {
            "name": exercise.name,
            "description": exercise.description,
            "image_id": image_id,
            "video_url": exercise.video_url,
        }
