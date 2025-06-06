from datetime import UTC, datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from common.models import LifeCycle
from domain.images.models import Image


class ChunkUpdate(BaseModel):
    content: str = Field(..., description="청크 내용")
    tags: List[str] = Field(default=[], description="청크 태그")


class ChunkEmbedding(BaseModel):
    embeded_state: bool = Field(default=False, description="청크 임베딩 상태")
    embeded_at: Optional[datetime] = Field(
        default=None,
        description="청크 임베딩 일시",
    )


class ChunkDetail(ChunkUpdate, ChunkEmbedding):
    page: int = Field(..., description="페이지 번호")
    file_creation_date: Optional[str] = Field(
        default=None,
        description="파일 생성 일시",
    )
    file_modification_date: Optional[str] = Field(
        default=None,
        description="파일 수정 일시",
    )


class Chunk(ChunkDetail, LifeCycle):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    document_id: ObjectId = Field(..., description="DOCUMENT ID")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class ChunkRequest(BaseModel):
    document_id: str = Field(..., description="문서 ID")
    chunk_size: int = Field(default=1024, description="청크 크기")
    chunk_overlap: int = Field(default=200, description="청크 중복")


class ChunkDetailResponse(Chunk):
    image_list: Optional[List[Image]] = Field(default=[], description="이미지 리스트")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
