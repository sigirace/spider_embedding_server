# application/documents/use_cases/create_document.py
import os
from typing import List, Tuple
from fastapi import HTTPException, UploadFile, status
from application.services.validator import Validator
from domain.documents.models import Document, DocumentErrorSchema
from domain.documents.repository import IDocumentRepository
from infra.service.file_storage_service import LocalFileStorageService
import logging

from utils.object_utils import get_str_id

logger = logging.getLogger(__name__)


class CreateDocument:
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
        app_id: str,
        file_list: List[UploadFile],
        user_id: str,
    ) -> Tuple[List[Document], List[DocumentErrorSchema]]:
        if not file_list:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="파일이 없습니다.",
            )

        existing_app = await self.validator.app_validator(app_id, user_id)

        success_list: List[Document] = []
        error_list: List[DocumentErrorSchema] = []

        for file in file_list:
            filename = file.filename or "no_name"
            try:

                extension = filename.rsplit(".", 1)[-1] if "." in filename else "etc"
                content_type = file.content_type or "application/octet-stream"
                root_folder = get_str_id(existing_app.id)
                relative_path = os.path.join(root_folder, extension, filename)

                # 1. 파일 내용 먼저 읽음
                content = await file.read()
                await file.seek(0)  # 나중에 재사용 가능성 대비

                size = file.size or len(content)

                # 2. 해시 계산
                file_hash = await self.fs.compute_hash(content)

                # 3. 중복 검사
                is_duplicate = await self.document_repository.exist_document(
                    app_id=existing_app.id,
                    hash=file_hash,
                    size=size,
                )

                if is_duplicate:
                    error_list.append(
                        DocumentErrorSchema(
                            name=filename,
                            error="중복된 문서입니다.",
                        )
                    )
                    continue

                # 4. 실제 저장
                file_path = await self.fs.save_bytes(content, relative_path)

                try:
                    # 5. DB 저장
                    document = Document(
                        name=filename,
                        hash=file_hash,
                        size=size,
                        type=content_type,
                        extension=extension,
                        app_id=existing_app.id,
                        file_path=file_path,
                        creator=user_id,
                    )
                    document.id = await self.document_repository.create(document)
                    success_list.append(document)
                except Exception as e:
                    await self.fs.move_to_trash(file_path)
                    raise HTTPException(
                        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                        detail=f"문서 생성 실패: {str(e)}",
                    )

            except Exception as e:
                logger.exception(
                    f"[PROCESS ERROR] 파일 처리 중 오류: {filename}, {str(e)}"
                )
                error_list.append(
                    DocumentErrorSchema(
                        name=filename,
                        error=f"파일 처리 중 오류가 발생했습니다.",
                    )
                )

        return success_list, error_list
