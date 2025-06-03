import asyncio
from typing import List
from langchain_core.embeddings import Embeddings

from domain.embeddings.api import IEmbedAPIRepository


class EmbedAPIError(RuntimeError):
    """임베딩 API 호출 실패"""


class EmbedAPIRepositoryImpl(IEmbedAPIRepository):
    def __init__(self, model: Embeddings):
        self._model = model

    async def embed_query(self, query: str) -> List[float]:
        try:
            # LangChain Embeddings 는 동기 ⇒ thread off-load
            return await asyncio.to_thread(self._model.embed_query, query)
        except Exception as e:
            raise EmbedAPIError(str(e)) from e
