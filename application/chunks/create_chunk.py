from typing import List
from fastapi import HTTPException
from application.services.chunker import Chunker
from application.services.deleter import Deleter
from application.services.validator import Validator
from domain.chunks.models import Chunk, ChunkRequest
from domain.chunks.repository import IChunkRepository
from infra.service.file_storage_service import LocalFileStorageService
from utils.document_utils import chunking


class CreateChunk:
    def __init__(
        self,
        chunk_repository: IChunkRepository,
        chunker: Chunker,
        validator: Validator,
        deleter: Deleter,
    ):
        self.chunk_repository = chunk_repository
        self.chunker = chunker
        self.validator = validator
        self.deleter = deleter

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
        chunk_list = await self.chunk_repository.get_by_document_id(
            document_id=document.id,
        )

        for chunk in chunk_list:
            await self.deleter.delete_chunk(chunk)

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
