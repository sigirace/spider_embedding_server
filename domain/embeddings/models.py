from enum import Enum
from datetime import UTC, datetime
from typing import List, Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class EmbedModelType(str, Enum):
    KURE = "kure"
    NOMIC = "nomic"


class EmbedSchema(BaseModel):
    text: str
    image_descriptions: List[str] = Field(default_factory=list)


class EmbeddingResultSchema(BaseModel):
    query: str
    embedding: List[float]


class Embedding(BaseModel):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    chunk_id: ObjectId
    embed_pk: str
    collection_name: str
    model_type: EmbedModelType
    creator: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC),
        description="생성 일시 (UTC, timezone-aware)",
    )

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class SearchEmbeddingSchema(BaseModel):
    query: str
    app_name: str
    k: int
    model_type: EmbedModelType
    user_id: str


class SearchResultSchema(BaseModel):
    chunk_id: str
    document_name: str
    page: int
    content: str
    tags: Optional[List[str]]
    file_creation_date: str
    file_modification_date: Optional[str]
