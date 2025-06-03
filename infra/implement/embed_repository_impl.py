from __future__ import annotations
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClientSession

from domain.embeddings.models import Embedding
from domain.embeddings.repository import IEmbedRepository

COLLECTION = "embedding"


class EmbedRepositoryImpl(IEmbedRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[COLLECTION]

    async def create(
        self,
        embedding: Embedding,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId:
        res = await self.collection.insert_one(
            embedding.model_dump(by_alias=True, exclude={"id"}), session=session
        )
        return res.inserted_id

    async def get(
        self,
        embed_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Embedding | None:
        doc = await self.collection.find_one({"_id": embed_id}, session=session)
        return Embedding.model_validate(doc) if doc else None

    async def get_by_chunk_id(
        self,
        chunk_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Embedding | None:
        doc = await self.collection.find_one({"chunk_id": chunk_id}, session=session)
        return Embedding.model_validate(doc) if doc else None

    async def delete(
        self,
        embed_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> None:
        await self.collection.delete_one({"_id": embed_id}, session=session)
