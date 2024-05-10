from abc import ABC, abstractmethod
from typing import Type

from database import async_session_maker
from repositories.images import ImagesRepository
from repositories.nutriton.meal_nutrients import MealNutrientsRepository
from repositories.nutriton.user_goal_nutrients import UserGoalNutrientsRepository
from repositories.users import UsersRepository
from repositories.workout.exercises import ExercisesRepository


class IUnitOfWork(ABC):
    users = Type[UsersRepository]
    meal_nutrients = Type[MealNutrientsRepository]
    user_goal_nutrients = Type[UserGoalNutrientsRepository]

    @abstractmethod
    def __init__(self) -> None: ...

    @abstractmethod
    async def __aenter__(self) -> None: ...

    @abstractmethod
    async def __aexit__(self, *args) -> None: ...

    @abstractmethod
    async def commit(self) -> None: ...

    @abstractmethod
    async def rollback(self) -> None: ...

    @abstractmethod
    async def refresh(self, obj) -> None: ...

    @abstractmethod
    async def close(self) -> None: ...


class UnitOfWork(IUnitOfWork):
    def __init__(self) -> None:
        self.session_factory = async_session_maker

    async def __aenter__(self) -> None:
        self.session = self.session_factory()

        self.users = UsersRepository(self.session)
        self.meal_nutrients = MealNutrientsRepository(self.session)
        self.user_goal_nutrients = UserGoalNutrientsRepository(self.session)
        self.exercises = ExercisesRepository(self.session)
        self.images = ImagesRepository(self.session)

    async def __aexit__(self, exc_type, exc_val, exc_tb) -> None:
        if exc_type:
            await self.rollback()
            print("EEEEEERRRORR")
        await self.session.close()

    async def commit(self) -> None:
        await self.session.commit()

    async def rollback(self) -> None:
        await self.session.rollback()

    async def refresh(self, obj):
        await self.session.refresh(obj)

    async def close(self):
        await self.session.close()
