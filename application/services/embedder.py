from datetime import UTC, datetime
from typing import Callable, List, Any
import uuid

from bson import ObjectId
from fastapi import HTTPException, status
from langchain_core.documents import Document

from common.uow import MongoUnitOfWork
from domain.chunks.models import Chunk
from domain.chunks.repository import IChunkRepository
from domain.embeddings.api import IEmbedAPIRepository
from domain.embeddings.models import Embedding, EmbedModelType, EmbedSchema
from domain.embeddings.repository import IEmbedRepository
from domain.vectors.repository import IVectorStoreRepository
from utils.object_utils import get_str_id
from langchain_core.embeddings import Embeddings


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
        if not schema.image_descriptions and not schema.text.strip():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Image descriptions and text are both empty",
            )

        parts = [f"{i+1}. {d}" for i, d in enumerate(schema.image_descriptions)]
        if schema.text.strip():
            parts.append(schema.text.strip())

        return "\n".join(parts).strip()

    async def aembed(
        self,
        query: str,
        embedding_model: IEmbedAPIRepository,
    ) -> List[float]:
        embed_list = await embedding_model.aembed_query(query)
        return embed_list

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

    async def retrieve(
        self,
        query: str,
        k: int,
        collection_name: str,
        model_type: str,
    ) -> List[Document]:
        store = self.vector_store_factory(collection_name)
        embedding_model = self._api_factory(model_type)
        store.override_embedding_function(embedding_model)
        return await store.similarity_search(query=query, k=k)

    async def execute(
        self,
        chunk: Chunk,
        embed_schema: EmbedSchema,
        model_type: str,
        user_id: str,
        collection_name: str,
    ) -> str:
        query = self.build_query(embed_schema)
        embedding_model = self._api_factory(model_type)
        vector = await self.aembed(query, embedding_model)
        store = self.vector_store_factory(collection_name)
        store.override_embedding_function(embedding_model)

        async with self._uow_factory() as uow:
            # 새로운 임베딩 저장
            embed_pk = await store.save(
                embedding=vector,
                chunk_id=get_str_id(chunk.id),
                metadata={
                    "model": model_type,
                },
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
