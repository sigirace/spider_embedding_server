from abc import ABC, abstractmethod
from typing import List
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorClientSession

from .models import Embedding


class IEmbedRepository(ABC):
    @abstractmethod
    async def create(
        self,
        embedding: Embedding,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId: ...

    @abstractmethod
    async def get(
        self,
        embed_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Embedding | None: ...

    @abstractmethod
    async def get_by_chunk_id(
        self,
        chunk_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Embedding | None: ...

    @abstractmethod
    async def delete(
        self,
        embed_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> None: ...
