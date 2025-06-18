from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class EmbedModelType(str, Enum):
    KURE = "kure"
    NOMIC = "nomic"


class EmbedRequest(BaseModel):
    model_type: EmbedModelType = Field(
        default=EmbedModelType.NOMIC,
        description="임베딩 모델 타입",
    )


class SearchRequest(BaseModel):
    app_name: str = Field(..., description="앱 이름")
    query: str = Field(..., description="검색 쿼리")
    k: Optional[int] = Field(default=3, description="검색 결과 개수")
    model_type: Optional[EmbedModelType] = Field(
        default=EmbedModelType.NOMIC,
        description="임베딩 모델 타입",
    )


class SearchResponse(BaseModel):
    chunk_id: str = Field(..., description="청크 ID")
    document_name: str = Field(..., description="문서 이름")
    page: int = Field(..., description="페이지 번호")
    content: str = Field(..., description="청크 내용")
    tags: Optional[List[str]] = Field(default_factory=list, description="청크 태그")
    file_creation_date: str = Field(..., description="파일 생성 시간")
    file_modification_date: Optional[str] = Field(
        default=None, description="파일 수정 시간"
    )


class SearchResponseList(BaseModel):
    search_response_list: List[SearchResponse] = Field(
        ..., description="검색 결과 리스트"
    )
