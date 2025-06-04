from datetime import UTC, datetime
from fastapi import HTTPException, status
from application.services.chunker import Chunker
from application.services.validator import Validator
from domain.chunks.models import Chunk, ChunkUpdate
from domain.chunks.repository import IChunkRepository


class UpdateChunk:
    def __init__(
        self,
        chunk_repository: IChunkRepository,
        chunker: Chunker,
        validator: Validator,
    ):
        self.validator = validator
        self.chunk_repository = chunk_repository
        self.chunker = chunker

    async def __call__(
        self,
        chunk_id: str,
        request: ChunkUpdate,
        user_id: str,
    ) -> Chunk:
        try:
            chunk = await self.validator.chunk_validator(chunk_id, user_id)
            chunk.content = request.content
            chunk.tags = request.tags
            chunk.updater = user_id
            chunk.updated_at = datetime.now(UTC)

            if chunk.embeded_state:
                chunk.embeded_state = False
                chunk.embeded_at = None

            await self.chunk_repository.update(chunk)

            chunk_detail = await self.chunker.get_chunk_detail(chunk)

            return chunk_detail
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
