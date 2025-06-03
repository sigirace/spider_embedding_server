from abc import ABC, abstractmethod
from typing import List, Any


class IVectorStoreRepository(ABC):
    @abstractmethod
    async def similarity_search(self, query: str, k: int) -> List[str]:
        """쿼리 문장을 입력받아 유사한 결과를 top-k 반환"""
        ...

    @abstractmethod
    async def save(
        self, text: str, embedding: List[float], metadata: dict[str, Any] = {}
    ) -> str:
        """텍스트 + 임베딩 + (선택적) 메타데이터를 저장하고, 해당 ID를 반환"""
        ...

    @abstractmethod
    async def delete(self, ids: List[str]):
        """저장된 ID를 삭제"""
        ...
