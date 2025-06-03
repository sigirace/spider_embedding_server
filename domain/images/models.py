from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field

from common.models import LifeCycle


class ImageDetail(BaseModel):
    image_path: str = Field(..., description="이미지 경로")
    image_description: Optional[str] = Field(None, description="이미지 설명")


class Image(LifeCycle, ImageDetail):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    chunk_id: ObjectId = Field(..., description="CHUNK ID")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class ImageUpdate(BaseModel):
    image_description: str = Field(..., description="이미지 설명")
