from typing import List
from application.services.embedder import Embedder
from application.services.validator import Validator
from domain.embeddings.models import SearchEmbeddingSchema, SearchResultSchema
from utils.object_utils import get_str_id


class SearchEmbedding:
    def __init__(
        self,
        embedder: Embedder,
        validator: Validator,
    ):
        self.embedder = embedder
        self.validator = validator

    async def __call__(
        self,
        search_embedding_schema: SearchEmbeddingSchema,
    ) -> List[SearchResultSchema]:

        app = await self.validator.app_name_validator(
            app_name=search_embedding_schema.app_name,
            user_id=search_embedding_schema.user_id,
        )

        collection_name = f"{search_embedding_schema.user_id}_{app.app_name}"

        results = await self.embedder.retrieve(
            query=search_embedding_schema.query,
            k=search_embedding_schema.k,
            collection_name=collection_name,
            model_type=search_embedding_schema.model_type,
        )

        result_list = []

        for result in results:
            try:
                chunk = await self.validator.chunk_validator(
                    chunk_id=result.page_content,
                    user_id=search_embedding_schema.user_id,
                )
                document = await self.validator.document_validator(
                    document_id=chunk.document_id,
                    user_id=search_embedding_schema.user_id,
                )

                result = SearchResultSchema(
                    chunk_id=get_str_id(chunk.id),
                    document_name=document.name,
                    page=chunk.page,
                    content=chunk.content,
                    tags=chunk.tags,
                    file_creation_date=chunk.file_creation_date,
                    file_modification_date=chunk.file_modification_date,
                )

                result_list.append(result)

            except Exception as e:
                continue

        return result_list
