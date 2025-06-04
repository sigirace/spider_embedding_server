from datetime import UTC, datetime
from typing import Callable, List, Any
import uuid

from bson import ObjectId

from common.uow import MongoUnitOfWork
from domain.chunks.models import Chunk
from domain.chunks.repository import IChunkRepository
from domain.embeddings.api import IEmbedAPIRepository
from domain.embeddings.models import Embedding, EmbedModelType, EmbedSchema
from domain.embeddings.repository import IEmbedRepository
from domain.vectors.repository import IVectorStoreRepository
from utils.object_utils import get_str_id


class Embedder:
    def __init__(
        self,
        embed_api_repo_factory: Callable[[str], IEmbedAPIRepository],
        embed_repository: IEmbedRepository,
        chunk_repository: IChunkRepository,
        vector_store_factory: Callable[[str], IVectorStoreRepository],
        uow_factory: Callable[[], MongoUnitOfWork],
    ):
        self._api_factory = embed_api_repo_factory
        self.embed_repository = embed_repository
        self.chunk_repository = chunk_repository
        self.vector_store_factory = vector_store_factory
        self._uow_factory = uow_factory

    @staticmethod
    def build_query(schema: EmbedSchema) -> str:
        parts = [f"{i+1}. {d}" for i, d in enumerate(schema.image_descriptions)]
        parts.append(schema.text)
        return "\n".join(parts).strip()

    async def embed(self, query: str, model_type: str) -> List[float]:
        api_repo = self._api_factory(model_type)
        return await api_repo.embed_query(query)

    async def delete_existing_embeddings(
        self,
        collection_name: str,
        ids: ObjectId,
        embed_id: ObjectId,
        chunk: Chunk,
    ) -> None:
        store = self.vector_store_factory(collection_name)
        async with self._uow_factory() as uow:
            await store.delete(ids=[get_str_id(ids)])
            await self.embed_repository.delete(embed_id, session=uow.session)
            chunk.embeded_state = False
            chunk.embeded_at = None
            await self.chunk_repository.update(chunk, session=uow.session)

    async def execute(
        self,
        chunk: Chunk,
        embed_schema: EmbedSchema,
        model_type: str,
        user_id: str,
        collection_name: str,
    ) -> str:
        query = self.build_query(embed_schema)
        vector = await self.embed(query, model_type)
        store = self.vector_store_factory(collection_name)

        async with self._uow_factory() as uow:
            # 새로운 임베딩 저장
            embed_pk = await store.save(
                text=query,
                embedding=vector,
                metadata={"chunk_id": str(chunk.id), "model": model_type},
            )
            record = Embedding(
                chunk_id=chunk.id,
                embed_pk=embed_pk,
                collection_name=collection_name,
                model_type=EmbedModelType(model_type),
                creator=user_id,
            )
            await self.embed_repository.create(
                record,
                session=uow.session,
            )
            chunk.embeded_state = True
            chunk.embeded_at = datetime.now(UTC)
            await self.chunk_repository.update(
                chunk,
                session=uow.session,
            )
        return embed_pk
