from abc import ABC, abstractmethod
from typing import Type, Any, Optional

from sqlalchemy import insert, select, update, delete
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from database import Base


class AbstractRepository(ABC):
    @abstractmethod
    async def add_one(self, data: dict):
        raise NotImplementedError

    @abstractmethod
    async def get_one(self, options: list | None = None, filter_by: dict | None = None):
        raise NotImplementedError

    @abstractmethod
    async def get_all(
        self,
        options: list | None = None,
        order_by: str | None = None,
        filter_by: dict | None = None,
    ) -> list | None:
        raise NotImplementedError

    @abstractmethod
    async def update_one(self, data: dict, _id: int):
        raise NotImplementedError

    @abstractmethod
    async def delete_one(self, _id: int):
        raise NotImplementedError


class SQLAlchemyRepository(AbstractRepository):
    model = Type[Base]  # type: ignore

    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_one(self, data: dict) -> int:
        stmt = insert(self.model).values(**data).returning(self.model.id)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar_one()

    async def get_all(
        self,
        options: list | None = None,
        order_by: str | None = None,
        filter_by: dict | None = None,
        group_by: list | None = None,
        select_by: list | None = None,
        where: Any = None,
    ):
        if select_by is None:
            select_by = [self.model]
        stmt = select(*select_by)  # type: ignore
        if filter_by is not None:
            stmt = stmt.filter_by(**filter_by)
        if where is not None:
            stmt = stmt.where(where)
        if options is not None:
            for entity in options:
                stmt = stmt.options(entity)
        if group_by is not None:
            stmt = stmt.group_by(*group_by)
        if order_by is not None:
            stmt = stmt.order_by(order_by)
        try:
            result = await self.session.execute(stmt)
            return result.fetchone()
        except NoResultFound:
            return None

    async def get_one(self, options: list | None = None, filter_by: dict | None = None):
        stmt = select(self.model).filter_by(**filter_by)  # type: ignore
        if options is not None:
            for entity in options:
                stmt = stmt.options(entity)
        try:
            result = await self.session.execute(stmt)
            return result.scalar_one()
        except NoResultFound:
            return None

    async def update_one(
        self, data: dict, _id: int, where_arg: Optional[dict] = None
    ) -> int:
        if where_arg is None:
            where_arg = (self.model.id == _id)  # type: ignore
        stmt = (
            update(self.model)  # type: ignore
            .where(where_arg)  # type: ignore
            .values(**data)  # type: ignore
            .returning(self.model.id)  # type: ignore
        )
        result = await self.session.execute(stmt)  # type: ignore
        return result.scalar_one() if result else None

    async def delete_one(self, _id: int) -> int:
        stmt = delete(self.model).where(self.model.id == _id).returning(self.model.id)  # type: ignore
        result = await self.session.execute(stmt)
        return result.scalar_one() if result else None
