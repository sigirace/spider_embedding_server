from abc import ABC, abstractmethod
from typing import List


class IEmbedRepository(ABC):
    @abstractmethod
    def embed_query(self, query: str) -> List[float]:
        pass
