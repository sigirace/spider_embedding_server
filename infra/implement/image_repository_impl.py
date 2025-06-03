from typing import List
from bson import ObjectId
from domain.images.models import Image
from domain.images.repository import IImageRepository

from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorClientSession,
)


COLLECTION_NAME = "image"


class ImageRepositoryImpl(IImageRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[COLLECTION_NAME]

    async def create(
        self,
        image: Image,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId:
        res = await self.collection.insert_one(
            image.model_dump(by_alias=True, exclude={"id"}),
            session=session,
        )
        return res.inserted_id

    async def get(
        self,
        image_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Image | None:
        d = await self.collection.find_one(
            {"_id": image_id},
            session=session,
        )
        return Image.model_validate(d) if d else None

    async def get_by_chunk_id(
        self,
        chunk_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> List[Image] | None:

        cur = self.collection.find(
            {"chunk_id": chunk_id},
            session=session,
        )
        return [Image.model_validate(doc) async for doc in cur]

    async def update(
        self,
        image: Image,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ):
        await self.collection.update_one(
            {"_id": image.id},
            {"$set": image.model_dump(by_alias=True, exclude={"id"})},
            session=session,
        )

    async def delete(
        self,
        image_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> bool | None:
        await self.collection.delete_one(
            {"_id": image_id},
            session=session,
        )

    async def delete_by_chunk_id(
        self,
        chunk_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> bool | None:
        await self.collection.delete_many(
            {"chunk_id": chunk_id},
            session=session,
        )
