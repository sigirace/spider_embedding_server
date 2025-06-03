from motor.motor_asyncio import AsyncIOMotorDatabase

from database.setup.set_app_index import app_indexes
from database.setup.set_document_index import document_indexes


async def set_all_indexes(db: AsyncIOMotorDatabase):
    await app_indexes(db)
    await document_indexes(db)
