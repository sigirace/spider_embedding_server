from typing import List
from fastapi import Form
from pydantic import BaseModel, Field
from common.models import LifeCycle


class DocumentUpdateRequest(BaseModel):
    name: str = Field(..., description="파일 이름")


class DocumentRepsonse(DocumentUpdateRequest, LifeCycle):
    id: str = Field(..., description="Document ID (문자열형 ObjectId)")
    app_id: str = Field(..., description="app id")
    hash: str = Field(..., description="파일의 해시값 (무결성 검사용)")
    size: int = Field(..., description="파일 크기 (단위: 바이트)")
    file_path: str = Field(..., description="파일이 저장된 경로 또는 URL")
    type: str = Field(..., description="파일의 유형 (예: document, image)")
    extension: str = Field(..., description="파일 확장자 (예: pdf, jpg)")


class DocumentUploadError(BaseModel):
    name: str = Field(..., description="파일 이름")
    error: str = Field(..., description="에러 메시지")


class DocumentUploadResponse(BaseModel):
    success: List[DocumentRepsonse] = Field(..., description="성공한 문서 목록")
    error: List[DocumentUploadError] = Field(..., description="실패한 문서 목록")
