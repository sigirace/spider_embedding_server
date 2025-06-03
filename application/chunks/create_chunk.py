from typing import List
from fastapi import HTTPException
from application.services.chunker import Chunker
from application.services.validator import Validator
from domain.chunks.models import Chunk, ChunkRequest
from domain.chunks.repository import IChunkRepository
from infra.service.file_storage_service import LocalFileStorageService
from utils.document_utils import chunking


class CreateChunk:
    def __init__(
        self,
        chunk_repository: IChunkRepository,
        file_storage_service: LocalFileStorageService,
        chunker: Chunker,
        validator: Validator,
    ):
        self.chunk_repository = chunk_repository
        self.fs = file_storage_service
        self.chunker = chunker
        self.validator = validator

    async def __call__(
        self,
        chunk_request: ChunkRequest,
        user_id: str,
    ):
        # document 유효성 검사
        document = await self.validator.document_validator(
            document_id=chunk_request.document_id,
            user_id=user_id,
        )

        # 지원 파일 확장자 검사
        if document.extension != "pdf":
            raise HTTPException(
                status_code=400,
                detail="현재 pdf 파일만 청크 생성 가능합니다.",
            )

        # 기존 청크 삭제
        await self.chunker.delete_meta(
            document=document,
        )

        # 청크 생성
        splited_documents = await self.chunker.make_chunks(
            document=document,
            chunk_size=chunk_request.chunk_size,
            chunk_overlap=chunk_request.chunk_overlap,
        )

        chunk_list: List[Chunk] = []

        for _chunk in splited_documents:

            chunk_list.append(
                await self.chunker.save(
                    document_id=chunk_request.document_id,
                    document=_chunk,
                    user_id=user_id,
                )
            )

        return chunk_list
