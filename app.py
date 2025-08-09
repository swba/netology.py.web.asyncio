from asyncio import TaskGroup
from typing import Callable

import aiohttp

import config
from crud import CrudManager
from models import Planet, Person
from schema import validate_data, PersonSchema, PlanetSchema


class App:
    """The main application that fetches and saves data in the database."""

    def __init__(self, crud: CrudManager):
        self.crud = crud

    @staticmethod
    async def request(url: str) -> dict | None:
        async with aiohttp.ClientSession() as session:
            print(f'Requesting {url}')
            async with session.get(url) as response:
                if response.ok:
                    return await response.json()
        return None

    async def fetch_items(self, url: str, details_method: Callable):
        """Fetches items from the SWAPI and saves them."""
        while url:
            if data := await self.request(url):
                # Fetch items one by one.
                async with TaskGroup() as tg:
                    tasks = []
                    for item in data.get('results', []):
                        if url := item.get('url', None):
                            tasks.append(tg.create_task(details_method(url)))
                # All items in this chunk are fetched, save them now.
                items = [task.result() for task in tasks if task.result()]
                await self.crud.save_multiple(items)
                # Prepare URL for the next page fetch, if any.
                url = data.get('next', None)

    async def fetch_planets(self):
        """Fetches all the planets from the SWAPI and saves them."""
        await self.fetch_items(config.INITIAL_PLANETS_URL, self.fetch_planet)

    async def fetch_people(self):
        """Fetches all the planets from the SWAPI and saves them."""
        await self.fetch_items(config.INITIAL_PEOPLE_URL, self.fetch_person)

    async def fetch_planet(self, url: str) -> Planet | None:
        """Fetches a single planet from the SWAPI."""
        if data := await self.request(url):
            try:
                data = data['result']
                planet_id = int(data['uid'])
                if data := validate_data(data['properties'], PlanetSchema):
                    return Planet(id=planet_id, **data)
            except (KeyError, ValueError):
                pass
        return None

    async def fetch_person(self, url: str) -> Person | None:
        """Fetches a single person from the SWAPI."""
        if data := await self.request(url):
            try:
                # Prepare person data.
                data = data['result']
                person_id = int(data['uid'])
                data = data['properties']
                if data := validate_data(data, PersonSchema):
                    data['homeworld_id'] = data['homeworld']
                    del data['homeworld']
                    return Person(id=person_id, **data)
            except (KeyError, ValueError):
                pass
        return None
