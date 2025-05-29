# common/uow.py
from __future__ import annotations
from typing import AsyncIterator
from motor.motor_asyncio import (
    AsyncIOMotorClient,
    AsyncIOMotorClientSession,
)


class MongoUnitOfWork:
    """
    모든 컬렉션을 하나의 Mongo 'multi-document transaction'으로 묶어
    원자적 커밋/롤백을 보장한다.
    사용 예:
        async with uow as session:
            await repo_a.add(..., session=session)
            await repo_b.update(..., session=session)
    """

    def __init__(self, client: AsyncIOMotorClient) -> None:
        self._client = client
        self._session: AsyncIOMotorClientSession | None = None

    # -------------------------------------------------
    async def __aenter__(self) -> AsyncIOMotorClientSession:
        self._session = await self._client.start_session()
        self._session.start_transaction()
        return self._session           # use-cases obtain the session here

    async def __aexit__(self, exc_type, exc, tb) -> None:
        try:
            if exc_type:
                await self._session.abort_transaction()   # rollback
            else:
                await self._session.commit_transaction()  # commit
        finally:
            await self._session.end_session()
            self._session = None
