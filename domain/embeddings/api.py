from abc import ABC, abstractmethod
from typing import List


class IEmbedAPIRepository(ABC):
    """외부 임베딩 API (HTTP·SDK 등) 인터페이스"""

    @abstractmethod
    async def embed_query(self, query: str) -> List[float]: ...
