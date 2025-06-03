from abc import ABC, abstractmethod
from typing import List
from bson import ObjectId
from domain.images.models import Image
from motor.motor_asyncio import AsyncIOMotorClientSession


class IImageRepository(ABC):
    @abstractmethod
    async def create(
        self,
        image: Image,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId: ...

    @abstractmethod
    async def get(
        self,
        image_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Image | None: ...

    @abstractmethod
    async def get_by_chunk_id(
        self,
        chunk_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> List[Image] | None: ...

    @abstractmethod
    async def update(
        self,
        image: Image,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ): ...

    @abstractmethod
    async def delete(
        self,
        image_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> bool | None: ...

    @abstractmethod
    async def delete_by_chunk_id(
        self,
        chunk_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> bool | None: ...
