from domain.chunks.models import Chunk, ChunkUpdate
from domain.chunks.models import ChunkDetailResponse as ChunkDetailResponseDomain
from interface.dto.chunk_dto import (
    ChunkDetailResponse,
    ChunkRequest,
    ChunkResponse,
    ChunkUpdateRequest,
)
from domain.chunks.models import ChunkRequest as ChunkRequestDomain
from interface.mapper.image_mapper import ImageMapper


class ChunkMapper:

    @staticmethod
    def to_domain(req: ChunkRequest, document_id: str) -> ChunkRequestDomain:
        return ChunkRequestDomain(
            document_id=document_id,
            chunk_size=req.chunk_size,
            chunk_overlap=req.chunk_overlap,
        )

    @staticmethod
    def to_update_domain(req: ChunkUpdateRequest) -> ChunkUpdate:
        return ChunkUpdate(
            content=req.content,
            tags=req.tags,
        )

    @staticmethod
    def to_response(chunk: Chunk) -> ChunkResponse:
        return ChunkResponse(
            id=str(chunk.id),
            content=chunk.content,
        )

    @staticmethod
    def to_detail_response(
        chunk_detail_response: ChunkDetailResponseDomain,
    ) -> ChunkDetailResponse:
        return ChunkDetailResponse(
            id=str(chunk_detail_response.id),
            content=chunk_detail_response.content,
            tags=chunk_detail_response.tags,
            page=chunk_detail_response.page,
            file_creation_date=chunk_detail_response.file_creation_date,
            file_modification_date=chunk_detail_response.file_modification_date,
            embeded_state=chunk_detail_response.embeded_state,
            image_list=[
                ImageMapper.to_response(image)
                for image in chunk_detail_response.image_list
            ],
        )
