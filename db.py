from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

import config

engine = create_async_engine(config.DB_URL_ASYNC)
DbSessionMaker = async_sessionmaker(bind=engine, expire_on_commit=False)

async def close_db():
    await engine.dispose()
