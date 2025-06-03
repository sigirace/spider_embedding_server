from abc import ABC, abstractmethod
from typing import List
from bson import ObjectId
from domain.apps.models import App
from motor.motor_asyncio import AsyncIOMotorClientSession


class IAppRepository(ABC):
    @abstractmethod
    async def create(
        self,
        app: App,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> ObjectId: ...

    @abstractmethod
    async def get(
        self,
        app_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> App | None: ...

    @abstractmethod
    async def duplicate_check(
        self,
        creator: str,
        app_name: str,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> bool: ...

    @abstractmethod
    async def list_by_creator(
        self,
        creator: str,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ) -> List[App]: ...

    @abstractmethod
    async def update(
        self,
        app_id: ObjectId,
        app: App,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ): ...

    @abstractmethod
    async def delete(
        self,
        app_id: ObjectId,
        *,
        session: AsyncIOMotorClientSession | None = None,
    ): ...
