from typing import TypeVar

from sqlalchemy import select, ColumnElement
from sqlalchemy.exc import IntegrityError, NoResultFound, MultipleResultsFound
from sqlalchemy.orm import sessionmaker

from models import BaseModel

T = TypeVar('T', bound=BaseModel)


class CrudManager:
    """A general CRUD manager for models."""

    def __init__(self, session: sessionmaker):
        self.session = session

    def get(self, model_cls: type[T], value: any, key: str = 'id') -> T | None:
        field: ColumnElement = getattr(model_cls, key)
        stmt = select(model_cls).where(field == value)
        with self.session() as session:
            try:
                return session.scalars(stmt).one()
            except (NoResultFound, MultipleResultsFound):
                return None

    def save(self, instance: T) -> bool:
        with self.session() as session:
            try:
                session.add(instance)
                session.commit()
                return True
            except IntegrityError:
                return False

    def delete(self, instance: T):
        with self.session() as session:
            session.delete(instance)
            session.commit()
