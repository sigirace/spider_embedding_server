from typing import List, Optional
from pydantic import BaseModel, Field
from interface.dto.image_dto import ImageResponse


class ChunkRequest(BaseModel):
    chunk_size: int = Field(default=500, description="청크 크기")
    chunk_overlap: int = Field(default=20, description="청크 중복")


class ChunkResponse(BaseModel):
    id: str = Field(..., description="청크 ID")
    content: str = Field(..., description="청크 내용")


class ChunkListRequest(ChunkRequest):
    document_id: List[str] = Field(..., description="문서 ID 리스트")


class ChunkErrorResponse(BaseModel):
    document_id: str = Field(..., description="문서 ID")
    error_message: str = Field(..., description="에러 메시지")


class ChunkListResponse(BaseModel):
    success_list: List[str] = Field(..., description="성공한 문서 ID 리스트")
    error_list: List[ChunkErrorResponse] = Field(
        ..., description="실패한 문서 ID 리스트"
    )


class ChunkDetailResponse(BaseModel):
    id: str = Field(..., description="청크 ID")
    content: str = Field(..., description="청크 내용")
    tags: List[str] = Field(..., description="청크 태그")
    page: int = Field(..., description="페이지 번호")
    file_creation_date: Optional[str] = Field(
        default=None,
        description="파일 생성 일시",
    )
    file_modification_date: Optional[str] = Field(
        default=None,
        description="파일 수정 일시",
    )
    embeded_state: bool = Field(..., description="청크 임베딩 상태")
    image_list: List[ImageResponse] = Field(..., description="이미지 리스트")


class ChunkUpdateRequest(BaseModel):
    content: str = Field(..., description="청크 내용")
    tags: List[str] = Field(default=[], description="청크 태그")
