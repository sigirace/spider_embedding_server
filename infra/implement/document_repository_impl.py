from typing import List
from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorClientSession,
)

from domain.documents.models import Document
from domain.documents.repository import IDocumentRepository

COLLECTION_NAME = "document"


class DocumentRepositoryImpl(IDocumentRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[COLLECTION_NAME]

    async def create(
        self,
        document: Document,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId:
        res = await self.collection.insert_one(
            document.model_dump(by_alias=True, exclude={"id"}),
            session=session,
        )
        return res.inserted_id

    async def get(
        self,
        document_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Document | None:
        d = await self.collection.find_one(
            {"_id": document_id},
            session=session,
        )
        return Document.model_validate(d) if d else None

    async def exist_document(
        self,
        app_id: ObjectId,
        hash: str,
        size: int,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> bool:
        cnt = await self.collection.count_documents(
            {"app_id": app_id, "hash": hash, "size": size},
            session=session,
        )
        return cnt > 0

    async def list_by_app_id(
        self,
        app_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> List[Document]:
        cur = self.collection.find(
            {"app_id": app_id},
            session=session,
        )
        return [Document.model_validate(doc) async for doc in cur]

    async def update(
        self,
        document_id: ObjectId,
        document: Document,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ):
        await self.collection.update_one(
            {"_id": document_id},
            {
                "$set": document.model_dump(
                    by_alias=True,
                    exclude={"id"},
                ),
            },
            session=session,
        )

    async def delete(
        self,
        document_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ):
        await self.collection.delete_one(
            {"_id": document_id},
            session=session,
        )
