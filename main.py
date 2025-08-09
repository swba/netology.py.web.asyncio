import asyncio

from app import App
from crud import CrudManager
from db import DbSessionMaker, close_db


async def main():
    crud = CrudManager(DbSessionMaker)
    app = App(crud)

    # First save all the planets.
    await app.fetch_planets()
    # And only then fetch and save people.
    await app.fetch_people()

    await close_db()

asyncio.run(main())
