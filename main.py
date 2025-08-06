import asyncio
from asyncio import TaskGroup

from app import App
from models import database

async def main():
    with database(True) as crud:
        # We first need to fetch all planets...
        async with TaskGroup() as tg:
            app = App(crud, tg)
            tg.create_task(app.fetch_planets())
        # ...and only then fetch people.
        async with TaskGroup() as tg:
            app = App(crud, tg)
            tg.create_task(app.fetch_people())

asyncio.run(main())
