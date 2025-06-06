from abc import ABC, abstractmethod
from typing import List, Any
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings


class IVectorStoreRepository(ABC):
    @abstractmethod
    async def similarity_search(self, query: str, k: int) -> List[Document]:
        """쿼리 문장을 입력받아 유사한 결과를 top-k 반환"""
        ...

    @abstractmethod
    async def save(
        self,
        embedding: List[float],
        chunk_id: str,
        metadata: dict[str, Any] = {},
    ) -> str:
        """임베딩 + (선택적) 메타데이터를 저장하고, 해당 ID를 반환"""
        ...

    @abstractmethod
    async def delete(self, ids: List[str]):
        """저장된 ID를 삭제"""
        ...

    @abstractmethod
    async def drop(self):
        """컬렉션 삭제"""
        ...

    @abstractmethod
    def override_embedding_function(self, new_func: Embeddings):
        """임베딩 함수 덮어쓰기"""
        ...
