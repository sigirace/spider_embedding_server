from abc import ABC, abstractmethod
from typing import List
from bson import ObjectId
from domain.documents.models import Document
from motor.motor_asyncio import AsyncIOMotorClientSession


class IDocumentRepository(ABC):
    @abstractmethod
    async def create(
        self,
        document: Document,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId: ...

    @abstractmethod
    async def get(
        self,
        document_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Document | None: ...

    @abstractmethod
    async def exist_document(
        self,
        app_id: ObjectId,
        hash: str,
        size: int,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> bool: ...

    @abstractmethod
    async def list_by_app_id(
        self,
        app_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> List[Document]: ...

    @abstractmethod
    async def update(
        self,
        document_id: ObjectId,
        document: Document,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ): ...

    @abstractmethod
    async def delete(
        self,
        document_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ): ...
