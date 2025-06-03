from fastapi import HTTPException
from application.services.chunker import Chunker
from application.services.validator import Validator
from domain.chunks.models import Chunk


class GetChunk:
    def __init__(
        self,
        chunker: Chunker,
        validator: Validator,
    ):
        self.validator = validator
        self.chunker = chunker

    async def __call__(
        self,
        chunk_id: str,
        user_id: str,
    ) -> Chunk:
        try:
            chunk = await self.validator.chunk_validator(
                chunk_id=chunk_id,
                user_id=user_id,
            )

            return await self.chunker.get_chunk_detail(chunk)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
