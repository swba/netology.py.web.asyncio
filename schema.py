import logging

import pydantic


class BaseSchema(pydantic.BaseModel):
    pass

class PlanetSchema(BaseSchema):
    climate: str | None = None
    surface_water: int | None = None
    name: str
    diameter: int | None = None
    rotation_period: int | None = None
    terrain: str | None = None
    gravity: str | None = None
    orbital_period: int | None = None
    population: int | None = None

    @pydantic.field_validator('surface_water', mode='before')
    @classmethod
    def validate_surface_water(cls, value: str) -> int:
        return _int_or_none(value)

    @pydantic.field_validator('diameter', mode='before')
    @classmethod
    def validate_diameter(cls, value: str) -> int:
        return _int_or_none(value)

    @pydantic.field_validator('rotation_period', mode='before')
    @classmethod
    def validate_rotation_period(cls, value: str) -> int:
        return _int_or_none(value)

    @pydantic.field_validator('orbital_period', mode='before')
    @classmethod
    def validate_orbital_period(cls, value: str) -> int:
        return _int_or_none(value)

    @pydantic.field_validator('population', mode='before')
    @classmethod
    def validate_population(cls, value: str) -> int:
        return _int_or_none(value)


class PersonSchema(BaseSchema):
    birth_year: str | None = None
    eye_color: str | None = None
    gender: str | None = None
    hair_color: str | None = None
    homeworld: int | None = None
    mass: int | None = None
    name: str
    skin_color: str | None = None

    @pydantic.field_validator('homeworld', mode='before')
    @classmethod
    def validate_homeworld(cls, value: str) -> int | None:
        return _int_or_none(value.split('/')[-1])

    @pydantic.field_validator('mass', mode='before')
    @classmethod
    def validate_mass(cls, value: str) -> int:
        return _int_or_none(value)


def validate_data(data: dict, model_class: type[BaseSchema]) -> dict | None:
    try:
        model = model_class(**data)
        return model.model_dump(exclude_unset=True)
    except pydantic.ValidationError as e:
        logging.error(e)


def _int_or_none(value: str) -> int | None:
    try:
        return int(value)
    except ValueError:
        return None
