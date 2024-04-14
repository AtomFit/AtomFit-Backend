from abc import ABC, abstractmethod
from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, options: list = None, filter_by=None):
        raise NotImplementedError

    @abstractmethod
    async def get_all(self, options: list = None, order_by=None, filter_by=None):
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, data: dict, _id: int):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, _id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = None

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all(self, options: list = None, order_by=None, filter_by=None) -> list | None:
        stmt = select(self.model)
        if filter is not None:
            stmt = stmt.filter_by(**filter_by)
        if options is not None:
            for entity in options:
                stmt = stmt.options(entity)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        try:
            result = await self.session.execute(stmt)
            return result.scalar().all()
        except NoResultFound:
            return None

    async def get_one(self, options: list = None, filter_by=None):
        stmt = select(self.model).filter_by(**filter_by)
        if options is not None:
            for entity in options:
                stmt = stmt.options(entity)
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except NoResultFound:
            return None

    async def update_one(self, data: dict, _id: int) -> int:
        stmt = (
            update(self.model)
            .where(self.model.id == _id)
            .values(**data)
            .returning(self.model.id)
        )
        result = await self.session.execute(stmt)
        return result.scalar_one() if result else None

    async def delete_one(self, _id: int) -> int:
        stmt = delete(self.model).where(self.model.id == _id).returning(self.model.id)
        result = await self.session.execute(stmt)
        return result.scalar_one() if result else None
