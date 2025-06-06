from config import get_settings
from infra.service.vector_store_service import MilvusService

settings = get_settings()


def create_vector_store(collection_name: str) -> MilvusService:
    return MilvusService(
        collection_name=collection_name,
        dim=settings.milvus.milvus_dim,
        connection_args={
            "host": settings.milvus.milvus_host,
            "port": settings.milvus.milvus_port,
            "secure": False,  # TLS 미사용
        },
        text_field="chunk_id",
    )
