import databases
import sqlalchemy

from src.config import settings

database = databases.Database(settings.database_url)


async def open_db():
    await database.connect()


async def close_db():
    await database.disconnect()