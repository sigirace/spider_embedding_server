from typing import List
from pydantic import BaseModel, Field


class ImageGeneratorErrorDTO(BaseModel):
    image_id: str = Field(..., description="이미지 ID")
    error: str = Field(..., description="에러 메시지")


class ChunkGeneratorErrorDTO(BaseModel):
    chunk_id: str = Field(..., description="청크 ID")
    error: str = Field(..., description="에러 메시지")


class DocumentGeneratorErrorDTO(BaseModel):
    document_id: str = Field(..., description="문서 ID")
    error: str = Field(..., description="에러 메시지")


class ImageListResponseDTO(BaseModel):
    image_list: List[str] = Field(..., description="성공한 Image 목록")
    failed: List[ImageGeneratorErrorDTO] = Field(..., description="실패한 Image 목록")


class ChunkListResponseDTO(BaseModel):
    chunk_list: List[str] = Field(..., description="성공한 Chunk 목록")
    image_list: List[str] = Field(..., description="성공한 Image 목록")
    failed: List[ChunkGeneratorErrorDTO] = Field(..., description="실패한 Chunk 목록")


class DocumentListResponseDTO(BaseModel):
    document_list: List[str] = Field(..., description="성공한 Document 목록")
    image_list: List[str] = Field(..., description="성공한 Image 목록")
    failed: List[DocumentGeneratorErrorDTO] = Field(
        ..., description="실패한 Document 목록"
    )
