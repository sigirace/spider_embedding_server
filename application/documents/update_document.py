from datetime import UTC, datetime
from pathlib import Path
from fastapi import HTTPException, status
from application.services.validator import Validator
from common.exceptions import FileServiceError
from domain.documents.models import Document, DocumentUpdate
from domain.documents.repository import IDocumentRepository
from infra.service.file_storage_service import LocalFileStorageService


class UpdateDocument:
    def __init__(
        self,
        document_repository: IDocumentRepository,
        file_storage_service: LocalFileStorageService,
        validator: Validator,
    ):
        self.document_repository = document_repository
        self.validator = validator
        self.fs = file_storage_service

    async def __call__(
        self,
        document_id: str,
        update_document: DocumentUpdate,
        user_id: str,
    ) -> Document:
        try:

            document = await self.validator.document_validator(
                document_id=document_id,
                user_id=user_id,
            )

            # 파일 이름 변경 -> OS Error
            old_path = document.file_path
            new_name = update_document.name + Path(old_path).suffix

            if update_document.name == document.name:
                return document

            new_path = str(Path(old_path).with_name(new_name))
            await self.fs.rename(old_path, new_path)

            # DB 반영
            # update field
            document.name = update_document.name
            document.file_path = new_path
            document.updater = user_id
            document.updated_at = datetime.now(UTC)

            await self.document_repository.update(
                document_id=document.id,
                document=update_document,
            )

            return document

        except HTTPException as e:
            raise
        except FileServiceError as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
        except Exception as e:

            await self.fs.rename(new_path, old_path)

            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
