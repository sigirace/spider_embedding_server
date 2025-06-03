from typing import List
from bson import ObjectId
from fastapi import HTTPException, status

from domain.documents.models import (
    Document,
    DocumentErrorSchema,
    DocumentUpdate,
)
from interface.dto.document_dto import (
    DocumentUpdateRequest,
    DocumentRepsonse,
    DocumentUpdateRequest,
    DocumentUploadError,
    DocumentUploadResponse,
)


class DocumentMapper:
    @staticmethod
    def to_update(req: DocumentUpdateRequest) -> DocumentUpdate:
        try:
            return DocumentUpdate(
                name=req.name,
            )
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="잘못된 형식의 document id입니다.",
            )

    @staticmethod
    def to_response(doc: Document) -> DocumentRepsonse:
        try:
            return DocumentRepsonse(
                id=str(doc.id),
                app_id=str(doc.app_id),
                name=doc.name,
                hash=doc.hash,
                size=doc.size,
                file_path=doc.file_path,
                type=doc.type,
                extension=doc.extension,
                created_at=doc.created_at.isoformat(),
                updated_at=doc.updated_at.isoformat() if doc.updated_at else None,
                creator=doc.creator,
                updater=doc.updater,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Document 응답 변환 실패: {str(e)}",
            )

    @staticmethod
    def to_upload_error(error: DocumentErrorSchema) -> DocumentUploadError:
        return DocumentUploadError(name=error.name, error=error.error)

    @staticmethod
    def to_upload_response(
        success_list: List[Document], error_list: List[DocumentErrorSchema]
    ) -> DocumentUploadResponse:
        return DocumentUploadResponse(
            success=[DocumentMapper.to_response(doc) for doc in success_list],
            error=[DocumentMapper.to_upload_error(err) for err in error_list],
        )
