from abc import ABC, abstractmethod
from typing import List
from bson import ObjectId
from domain.chunks.models import Chunk
from motor.motor_asyncio import AsyncIOMotorClientSession


class IChunkRepository(ABC):
    @abstractmethod
    async def create(
        self,
        chunk: Chunk,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId: ...

    @abstractmethod
    async def get(
        self,
        chunk_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Chunk | None: ...

    @abstractmethod
    async def get_by_document_id(
        self,
        document_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> List[Chunk] | None: ...

    @abstractmethod
    async def update(
        self,
        chunk: Chunk,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ): ...

    @abstractmethod
    async def delete_by_document_id(
        self,
        document_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ): ...
