from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection
from .config import settings

_motor_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


def get_db() -> AsyncIOMotorDatabase:
    if _db is None:
        raise RuntimeError("Database not initialized")
    return _db


def get_collection(name: str) -> AsyncIOMotorCollection:
    return get_db()[name]


async def connect_to_mongo() -> None:
    global _motor_client, _db
    _motor_client = AsyncIOMotorClient(settings.mongo_uri)
    _db = _motor_client[settings.mongo_db_name]


async def close_mongo_connection() -> None:
    global _motor_client, _db
    if _motor_client is not None:
        _motor_client.close()
    _motor_client = None
    _db = None