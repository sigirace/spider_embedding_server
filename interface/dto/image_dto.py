from typing import Optional
from pydantic import BaseModel, Field


class ImageResponse(BaseModel):
    id: str = Field(..., description="이미지 ID")
    chunk_id: str = Field(..., description="청크 ID")
    image_path: str = Field(..., description="이미지 파일 경로")
    image_description: Optional[str] = Field(default=None, description="이미지 설명")


class ImageUpdateRequest(BaseModel):
    image_description: str = Field(..., description="이미지 설명")
