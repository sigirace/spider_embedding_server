from typing import List
import requests
from langchain_core.embeddings import Embeddings

from config import get_settings

haiqv_setting = get_settings().haiqv

HAIQV_NOMIC_EMBEDDING_URL = haiqv_setting.haiqv_embed_nomic_url
HAIQV_NOMIC_EMBEDDING_MODEL = haiqv_setting.haiqv_embed_nomic_model


class HaiqvNomicEmbedding(Embeddings):
    """Custom embedding class for HTTP-based APIs like nomic v2."""

    base_url: str = HAIQV_NOMIC_EMBEDDING_URL
    model: str = HAIQV_NOMIC_EMBEDDING_MODEL

    def embed_query(self, text: str) -> List[float]:
        try:
            response = requests.post(
                f"{self.base_url}/api/embeddings",
                json={"model": self.model, "prompt": text},
                timeout=10,
            )
            response.raise_for_status()
            return response.json()["embedding"]
        except Exception as e:
            raise RuntimeError(f"Nomic embedding API error: {e}") from e

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self.embed_query(text) for text in texts]
