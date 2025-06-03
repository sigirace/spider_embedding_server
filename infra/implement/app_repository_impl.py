# infra/repositories/app_repository_impl.py
from typing import Sequence
from bson import ObjectId
from motor.motor_asyncio import (
    AsyncIOMotorDatabase,
    AsyncIOMotorClientSession,
)

from domain.apps.models import App
from domain.apps.repository import IAppRepository

COLLECTION_NAME = "app"


class AppRepositoryImpl(IAppRepository):
    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db[COLLECTION_NAME]

    async def create(
        self,
        app: App,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId:
        res = await self.collection.insert_one(
            app.model_dump(by_alias=True, exclude={"id"}),
            session=session,
        )
        return res.inserted_id

    async def get(
        self, app_id: ObjectId, *, session: AsyncIOMotorClientSession | None = None
    ) -> App | None:
        d = await self.collection.find_one({"_id": app_id}, session=session)
        return App.model_validate(d) if d else None

    async def duplicate_check(
        self,
        creator: str,
        app_name: str,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> bool:
        d = await self.collection.find_one(
            {"creator": creator, "app_name": app_name}, session=session
        )
        return d is not None

    async def list_by_creator(
        self,
        creator: str,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> Sequence[App]:
        cur = self.collection.find({"creator": creator}, session=session)
        return [App.model_validate(doc) async for doc in cur]

    async def update(
        self,
        app_id: ObjectId,
        app: App,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ):
        await self.collection.replace_one(
            {"_id": app_id},
            app.model_dump(
                by_alias=True,
                exclude={"id"},
            ),
            session=session,
        )

    async def delete(
        self,
        app_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ):
        await self.collection.delete_one({"_id": app_id}, session=session)
