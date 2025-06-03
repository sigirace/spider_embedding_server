from typing import List
from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorClientSession,
)

from domain.chunks.models import Chunk
from domain.chunks.repository import IChunkRepository


COLLECTION_NAME = "chunk"


class ChunkRepositoryImpl(IChunkRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[COLLECTION_NAME]

    async def create(
        self,
        chunk: Chunk,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId:
        res = await self.collection.insert_one(
            chunk.model_dump(
                by_alias=True,
                exclude={"id"},
            ),
            session=session,
        )
        return res.inserted_id

    async def get(
        self,
        chunk_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Chunk | None:
        d = await self.collection.find_one(
            {"_id": chunk_id},
            session=session,
        )
        return Chunk.model_validate(d) if d else None

    async def get_by_document_id(
        self,
        document_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> List[Chunk] | None:
        cur = self.collection.find(
            {"document_id": document_id},
            session=session,
        )
        return [Chunk.model_validate(doc) async for doc in cur]

    async def update(
        self,
        chunk: Chunk,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> None:
        await self.collection.update_one(
            {"_id": chunk.id},
            {
                "$set": chunk.model_dump(
                    by_alias=True,
                    exclude={"id"},
                ),
            },
            session=session,
        )

    async def delete_by_document_id(
        self,
        document_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> None:
        await self.collection.delete_many(
            {"document_id": document_id},
            session=session,
        )
