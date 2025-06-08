import asyncio
import uuid
from typing import Any, Callable, Dict, List
from langchain_core.documents import Document
from langchain_milvus import Milvus as LangchainMilvus
import numpy as np
from domain.vectors.repository import IVectorStoreRepository
from pymilvus import (
    connections,
    utility,
    Collection,
    FieldSchema,
    CollectionSchema,
    DataType,
)
from langchain_core.embeddings import Embeddings

# 기본 벡터 인덱스 설정
_INDEX_PARAMS = {
    "index_type": "IVF_FLAT",
    "metric_type": "L2",
    "params": {"nlist": 1024},
}


class DummyEmbeddingFunction:
    def aembed_query(self, text: str) -> List[float]:
        # 테스트용 또는 기본용
        return [0.0] * 768  # 또는 self.embedding_model.aembed_query(text)


class MilvusService(IVectorStoreRepository):
    """
    - 컬렉션이 없으면 자동 생성
    - 벡터 삽입은 PyMilvus, 검색은 LangChain Milvus로 처리
    """

    def __init__(
        self,
        collection_name: str,
        dim: int,
        connection_args: Dict[str, Any],
        embedding_function: Callable | None = None,  # 추가
        text_field: str = "chunk_id",
    ):
        self.collection_name = collection_name
        self.dim = dim

        # 공통 alias 지정
        self._alias = "default"

        # pymilvus 연결
        connections.connect(alias=self._alias, **connection_args)

        # 존재하지 않으면 컬렉션 생성
        if not utility.has_collection(self.collection_name, using=self._alias):
            self._create_collection()

        # pymilvus 컬렉션 객체 (삽입용)
        self._collection = Collection(name=self.collection_name, using=self._alias)
        self._collection.load()

        self.embedding_function = embedding_function or DummyEmbeddingFunction()

        # langchain Milvus (검색용)
        self.store = LangchainMilvus(
            embedding_function=self.embedding_function,
            collection_name=self.collection_name,
            connection_args={
                "uri": f"http://{connection_args['host']}:{connection_args['port']}",
                "secure": connection_args.get("secure", False),
            },
            text_field=text_field,
        )

    async def similarity_search(
        self,
        query: str,
        k: int,
    ) -> List[Document]:
        return await asyncio.to_thread(
            self.store.similarity_search,
            query,
            k=k,
        )

    async def save(
        self,
        embedding: List[float],
        chunk_id: str,
        metadata: Dict[str, Any] | None = None,
    ) -> str:

        pk = np.int64(uuid.uuid4().int & ((1 << 63) - 1))

        await asyncio.to_thread(
            self._collection.insert,
            [
                [pk],  # id
                [embedding],  # vector
                [chunk_id],  # chunk_id
                [metadata or {}],  # metadata
            ],
        )

        await asyncio.to_thread(self._collection.flush)
        return str(pk)

    async def delete(self, ids: List[str]):
        int_ids = [int(i) for i in ids]
        expr = f"id in {int_ids}"
        await asyncio.to_thread(self._collection.delete, expr)
        await asyncio.to_thread(self._collection.flush)

    async def drop(self):
        """
        컬렉션이 존재하면 삭제
        """
        if await asyncio.to_thread(
            utility.has_collection,
            self.collection_name,
            using=self._alias,
        ):
            await asyncio.to_thread(
                utility.drop_collection,
                self.collection_name,
                using=self._alias,
            )

    # 내부 메서드
    def _create_collection(self):
        id_field = FieldSchema(
            name="id", dtype=DataType.INT64, is_primary=True, auto_id=False
        )
        vector_field = FieldSchema(
            name="vector", dtype=DataType.FLOAT_VECTOR, dim=self.dim
        )
        chunk_id_field = FieldSchema(
            name="chunk_id", dtype=DataType.VARCHAR, max_length=255
        )
        meta_field = FieldSchema(name="metadata", dtype=DataType.JSON)

        schema = CollectionSchema(
            fields=[id_field, vector_field, chunk_id_field, meta_field]
        )

        col = Collection(name=self.collection_name, schema=schema, using=self._alias)
        col.create_index(field_name="vector", index_params=_INDEX_PARAMS)
        col.load()

    def override_embedding_function(self, new_func: Embeddings):
        self.embedding_function = new_func
        self.store.embedding_func = new_func
