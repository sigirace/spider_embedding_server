from typing import List
from domain.llms.models import (
    ChunkGeneratorError,
    DocumentGeneratorError,
    ImageGeneratorError,
)

from interface.dto.llm_dto import (
    ChunkGeneratorErrorDTO,
    ChunkListResponseDTO,
    DocumentGeneratorErrorDTO,
    DocumentListResponseDTO,
    ImageGeneratorErrorDTO,
    ImageListResponseDTO,
)


class LlmMapper:
    @staticmethod
    def to_image_generator_error(error: ImageGeneratorError) -> ImageGeneratorErrorDTO:
        return ImageGeneratorErrorDTO(
            image_id=error.image_id,
            error=error.error,
        )

    @staticmethod
    def to_image_list_response(
        image_list: List[str],
        failed: List[ImageGeneratorError],
    ) -> ImageListResponseDTO:
        return ImageListResponseDTO(
            image_list=image_list,
            failed=[LlmMapper.to_image_generator_error(error) for error in failed],
        )

    @staticmethod
    def to_chunk_generator_error(error: ChunkGeneratorError) -> ChunkGeneratorErrorDTO:
        return ChunkGeneratorErrorDTO(
            chunk_id=error.chunk_id,
            error=error.error,
        )

    @staticmethod
    def to_chunk_list_response(
        chunk_list: List[str],
        image_list: List[str],
        failed_chunk_list: List[ChunkGeneratorError],
        failed_image_list: List[ImageGeneratorError],
    ) -> ChunkListResponseDTO:
        return ChunkListResponseDTO(
            chunk_list=chunk_list,
            image_list=image_list,
            failed_chunk_list=[
                LlmMapper.to_chunk_generator_error(error) for error in failed_chunk_list
            ],
            failed_image_list=[
                LlmMapper.to_image_generator_error(error) for error in failed_image_list
            ],
        )

    @staticmethod
    def to_document_generator_error(
        error: DocumentGeneratorError,
    ) -> DocumentGeneratorErrorDTO:
        return DocumentGeneratorErrorDTO(
            document_id=error.document_id,
            error=error.error,
        )

    @staticmethod
    def to_document_list_response(
        document_list: List[str],
        image_list: List[str],
        failed: List[DocumentGeneratorError],
    ) -> DocumentListResponseDTO:
        return DocumentListResponseDTO(
            document_list=document_list,
            image_list=image_list,
            failed=[LlmMapper.to_document_generator_error(error) for error in failed],
        )
