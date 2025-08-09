from typing import TypeVar

from sqlalchemy import select, ColumnElement
from sqlalchemy.exc import NoResultFound, MultipleResultsFound, IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.ext.asyncio import async_sessionmaker

from models import BaseModel

T = TypeVar('T', bound=BaseModel)


class CrudManager:
    """A general CRUD manager for models."""

    def __init__(self, session_maker: async_sessionmaker):
        self.session_maker: async_sessionmaker = session_maker

    async def get(self, model_cls: type[T], value: int) -> T | None:
        field: ColumnElement = getattr(model_cls, 'id')
        stmt = select(model_cls).where(field == value)
        async with self.session_maker() as session: # type: AsyncSession
            try:
                result = await session.execute(stmt)
                return result.scalars().one()
            except (NoResultFound, MultipleResultsFound):
                return None

    async def get_multiple(self, model_cls: type[T], values: list[int]) -> dict[int: T]:
        field: ColumnElement = getattr(model_cls, 'id')
        stmt = select(model_cls).where(field.in_(values))
        async with self.session_maker() as session: # type: AsyncSession
            results = await session.execute(stmt)
            return {item.id: item for item in results.scalars()}

    async def save(self, instance: T):
        async with self.session_maker() as session: # type: AsyncSession
            try:
                async with session.begin():
                    session.add(instance)
            except IntegrityError:
                pass

    async def save_multiple(self, instances: list[T]):
        async with self.session_maker() as session: # type: AsyncSession
            try:
                async with session.begin():
                    session.add_all(instances)
            except IntegrityError:
                pass

    async def delete(self, instance: T):
        async with self.session_maker() as session: # type: AsyncSession
            await session.delete(instance)
            await session.commit()
