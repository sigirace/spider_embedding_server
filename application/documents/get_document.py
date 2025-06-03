from fastapi import HTTPException
from application.services.validator import Validator
from domain.documents.repository import IDocumentRepository
from domain.documents.models import Document


class GetDocument:
    def __init__(
        self,
        document_repository: IDocumentRepository,
        validator: Validator,
    ):
        self.document_repository = document_repository
        self.validator = validator

    async def __call__(
        self,
        document_id: str,
        user_id: str,
    ) -> Document:
        try:
            return await self.validator.document_validator(
                document_id=document_id,
                user_id=user_id,
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
