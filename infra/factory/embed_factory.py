from domain.embeddings.api import IEmbedAPIRepository
from infra.wrapper.haiqv_kure_embedding import HaiqvKureEmbedding
from infra.wrapper.haiqv_nomic_embedding import HaiqvNomicEmbedding
from infra.api.embed_api_repository_impl import EmbedAPIRepositoryImpl

EMBED_MODEL_REGISTRY = {
    "kure": HaiqvKureEmbedding,
    "nomic": HaiqvNomicEmbedding,
}


def create_embed_api_repo(model_type: str | None = None) -> IEmbedAPIRepository:
    """
    모델 이름(kure, nomic)을 받아 EmbedAPIRepositoryImpl 인스턴스를 생성해 반환.

    >>> repo = create_embed_api_repo("kure")
    >>> vector = await repo.aembed_query("안녕")
    """
    key = (model_type or "kure").lower()

    if key not in EMBED_MODEL_REGISTRY:
        raise ValueError(f"지원하지 않는 임베딩 모델: {model_type}")

    embedding_model_cls = EMBED_MODEL_REGISTRY[key]
    embedding_model = embedding_model_cls()  # 필요 파라미터가 있으면 DI
    return EmbedAPIRepositoryImpl(embedding_model)
