from bson import ObjectId
from pydantic import BaseModel, Field
from common.models import LifeCycle  # created_at, updated_at, creator, updater 등 포함


class DocumentDetail(BaseModel):
    name: str = Field(..., description="파일 이름")
    hash: str = Field(..., description="파일의 해시값 (무결성 검사용)")
    size: int = Field(..., description="파일 크기 (단위: 바이트)")
    file_path: str = Field(default="", description="파일이 저장된 경로 또는 URL")
    type: str = Field(..., description="파일의 유형 (예: application/pdf)")
    extension: str = Field(..., description="파일 확장자 (예: pdf, jpg)")


class Document(DocumentDetail, LifeCycle):

    id: ObjectId = Field(default_factory=ObjectId, alias="_id")
    app_id: ObjectId = Field(..., description="앱 ID")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True


class DocumentUpdate(BaseModel):
    name: str = Field(..., description="파일 이름")


class DocumentErrorSchema(BaseModel):
    name: str = Field(..., description="파일 이름")
    error: str = Field(..., description="에러 메시지")
