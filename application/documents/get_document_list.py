from typing import List
from fastapi import HTTPException, status
from application.services.validator import Validator
from domain.documents.models import Document
from domain.documents.repository import IDocumentRepository


class GetDocumentList:
    def __init__(
        self,
        document_repository: IDocumentRepository,
        validator: Validator,
    ):
        self.document_repository = document_repository
        self.validator = validator

    async def __call__(
        self,
        app_id: str,
        user_id: str,
    ) -> List[Document]:
        try:
            app = await self.validator.app_validator(app_id, user_id)

            documents = await self.document_repository.list_by_app_id(app.id)

            if not documents:
                return []
            return documents

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
