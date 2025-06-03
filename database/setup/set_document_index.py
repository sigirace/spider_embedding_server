from motor.motor_asyncio import AsyncIOMotorDatabase

COLLECTION_NAME = "document"


async def document_indexes(db: AsyncIOMotorDatabase):
    await db[COLLECTION_NAME].create_index(
        [("app_id", 1), ("hash", 1), ("size", 1)],
        unique=True,
        name="app_id_hash_size_unique",
    )
