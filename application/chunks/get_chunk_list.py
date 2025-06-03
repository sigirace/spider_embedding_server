from typing import List
from fastapi import HTTPException, status
from application.services.validator import Validator
from domain.chunks.models import Chunk
from domain.chunks.repository import IChunkRepository


class GetChunkList:
    def __init__(
        self,
        chunk_repository: IChunkRepository,
        validator: Validator,
    ):
        self.chunk_repository = chunk_repository
        self.validator = validator

    async def __call__(
        self,
        document_id: str,
        user_id: str,
    ) -> List[Chunk]:
        try:
            document = await self.validator.document_validator(document_id, user_id)

            chunks = await self.chunk_repository.get_by_document_id(document.id)

            if not chunks:
                return []
            return chunks

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
