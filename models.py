from sqlalchemy import String, ForeignKey, BigInteger
from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    relationship,
    DeclarativeBase
)


class BaseModel(DeclarativeBase, AsyncAttrs):
    id: Mapped[int] = mapped_column(primary_key=True)


class Planet(BaseModel):
    """A Star Wars planet model."""
    __tablename__ = "planet"

    climate: Mapped[str] = mapped_column(String(30), nullable=True)
    surface_water: Mapped[int] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    diameter: Mapped[int] = mapped_column(nullable=True)
    rotation_period: Mapped[int] = mapped_column(nullable=True)
    terrain: Mapped[str] = mapped_column(String(100), nullable=True)
    gravity: Mapped[str] = mapped_column(String(100), nullable=True)
    orbital_period: Mapped[int] = mapped_column(nullable=True)
    population: Mapped[int] = mapped_column(BigInteger(), nullable=True)
    people: Mapped[list['Person']] = relationship(
        back_populates='homeworld',
        cascade = 'all, delete-orphan')


class Person(BaseModel):
    """A Star Wars person model."""
    __tablename__ = 'person'

    birth_year: Mapped[str] = mapped_column(String(10), nullable=True)
    eye_color: Mapped[str] = mapped_column(String(30), nullable=True)
    gender: Mapped[str] = mapped_column(String(30), nullable=True)
    hair_color: Mapped[str] = mapped_column(String(30), nullable=True)
    homeworld_id: Mapped[int] = mapped_column(ForeignKey('planet.id'), nullable=True)
    homeworld: Mapped['Planet'] = relationship(back_populates='people')
    mass: Mapped[int] = mapped_column(nullable=True)
    name: Mapped[str] = mapped_column(String(100))
    skin_color: Mapped[str] = mapped_column(String(30), nullable=True)
