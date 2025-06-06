from typing import List
from domain.embeddings.models import SearchEmbeddingSchema, SearchResultSchema
from interface.dto.embedding_dto import (
    SearchRequest,
    SearchResponse,
    SearchResponseList,
)


class EmbeddingMapper:
    @staticmethod
    def to_request(
        search_request: SearchRequest,
        user_id: str,
    ) -> SearchEmbeddingSchema:
        return SearchEmbeddingSchema(
            query=search_request.query,
            app_name=search_request.app_name,
            k=search_request.k,
            model_type=search_request.model_type,
            user_id=user_id,
        )

    @staticmethod
    def to_response_item(
        search_result: SearchResultSchema,
    ) -> SearchResponse:
        return SearchResponse(
            chunk_id=search_result.chunk_id,
            document_name=search_result.document_name,
            page=search_result.page,
            content=search_result.content,
            tags=search_result.tags,
            file_creation_date=search_result.file_creation_date,
            file_modification_date=search_result.file_modification_date,
        )

    @staticmethod
    def to_response(
        search_result_list: List[SearchResultSchema],
    ) -> SearchResponseList:
        return SearchResponseList(
            search_response_list=[
                EmbeddingMapper.to_response_item(search_result)
                for search_result in search_result_list
            ],
        )
