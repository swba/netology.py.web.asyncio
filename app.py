from asyncio import TaskGroup

import aiohttp

from crud import CrudManager
from models import Planet, Person
from schema import validate_data, PersonSchema, PlanetSchema


class App:
    """The main application that fetches and saves data in the database."""

    INITIAL_PEOPLE_URL = 'https://www.swapi.tech/api/people'
    INITIAL_PLANETS_URL = 'https://www.swapi.tech/api/planets'

    def __init__(self, crud: CrudManager, tg: TaskGroup):
        self.crud = crud
        self.tg = tg

    async def start(self):
        await self.tg.create_task(self.fetch_people())

    @staticmethod
    async def request(url: str) -> dict | None:
        async with aiohttp.ClientSession() as session:
            print(f'Requesting {url}')
            async with session.get(url) as response:
                if response.ok:
                    return await response.json()
        return None

    async def fetch_planets(self, url: str = INITIAL_PLANETS_URL):
        """Fetches a list of planets from the SWAPI."""
        if data := await self.request(url):
            # Fetch planets one by one.
            for item in data.get('results', []):
                if url := item.get('url', None):
                    self.tg.create_task(self.fetch_planet(url))
            # Schedule fetching the next page, if any.
            if next_url := data.get('next', None):
                # noinspection PyTypeChecker
                self.tg.create_task(self.fetch_planets(next_url))

    async def fetch_planet(self, url: str):
        """Fetches a planet from the SWAPI and saves it to the database."""
        if data := await self.request(url):
            try:
                # Fetch planet data.
                data = data['result']
                planet_id = data['uid']
                data = data['properties']
                # Validate planet data and save it to the database.
                data = validate_data(data, PlanetSchema)
                planet = Planet(id=planet_id, **data)
                self.crud.save(planet)
            except (KeyError, ValueError):
                pass

    async def fetch_people(self, url: str = INITIAL_PEOPLE_URL):
        """Fetches a list of people from the SWAPI."""
        if data := await self.request(url):
            # Fetch people one by one.
            for item in data.get('results', []):
                if url := item.get('url', None):
                    self.tg.create_task(self.fetch_person(url))
            # Schedule fetching the next page, if any.
            if next_url := data.get('next', None):
                # noinspection PyTypeChecker
                self.tg.create_task(self.fetch_people(next_url))

    async def fetch_person(self, url: str):
        """Fetches a person from the SWAPI and saves it in the database."""
        if data := await self.request(url):
            try:
                # Prepare person data.
                data = data['result']
                person_id = data['uid']
                data = data['properties']
                data = validate_data(data, PersonSchema)

                # Check planet and get its instance.
                if homeworld_id := data.pop('homeworld', None):
                    if homeworld := self.crud.get(Planet, homeworld_id):
                        data['homeworld'] = homeworld

                # Create and save a person instance.
                person = Person(id=person_id, **data)
                self.crud.save(person)
            except (KeyError, ValueError):
                pass
