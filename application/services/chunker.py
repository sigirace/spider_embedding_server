from __future__ import annotations

from typing import Callable, List
from fastapi import HTTPException, status
from langchain_core.documents import Document as LangDocument
from motor.motor_asyncio import AsyncIOMotorClientSession

from domain.chunks.models import Chunk, ChunkDetailResponse
from domain.chunks.repository import IChunkRepository
from domain.images.models import Image
from domain.images.repository import IImageRepository
from domain.documents.models import Document
from infra.service.file_storage_service import LocalFileStorageService
from common.uow import MongoUnitOfWork
from utils.date_utils import parse_pdf_date
from utils.document_utils import chunking
from utils.object_utils import get_object_id, get_str_id


class Chunker:
    """1) 파일을 청크로 분할  2) 각 청크와 이미지 메타를 원자적으로 저장"""

    def __init__(
        self,
        chunk_repository: IChunkRepository,
        image_repository: IImageRepository,
        file_storage_service: LocalFileStorageService,
        uow_factory: Callable[[], MongoUnitOfWork],
    ) -> None:
        self.chunk_repository = chunk_repository
        self.image_repository = image_repository
        self.fs = file_storage_service
        self._uow_factory = uow_factory

    async def get_chunk_detail(
        self,
        chunk: Chunk,
    ) -> ChunkDetailResponse:

        image_list = await self.image_repository.get_by_chunk_id(chunk_id=chunk.id)

        return ChunkDetailResponse(
            **chunk.model_dump(by_alias=True),
            image_list=image_list or [],
        )

    async def make_chunks(
        self,
        document: Document,
        chunk_size: int,
        chunk_overlap: int,
    ) -> List[LangDocument]:
        try:
            img_path = await self.fs.get_image_path(
                app_id=get_str_id(document.app_id),
                document_id=get_str_id(document.id),
            )
            return chunking(
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
                file_path=document.file_path,
                image_path=img_path,
            )
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Document pre-processing 오류: {e}",
            ) from e

    async def save(
        self,
        document_id: str,
        document: LangDocument,
        user_id: str,
    ) -> Chunk:
        try:
            async with self._uow_factory() as uow:
                oid = get_object_id(document_id)
                chunk = Chunk(
                    document_id=oid,
                    content=document.page_content,
                    tags=document.metadata.get("tags", []),
                    page=document.metadata.get("page", 0),
                    file_creation_date=parse_pdf_date(
                        document.metadata.get("creationDate")
                    ),
                    file_modification_date=parse_pdf_date(
                        document.metadata.get("modDate")
                    ),
                    creator=user_id,
                )

                chunk.id = await self.chunk_repository.create(
                    chunk,
                    session=uow.session,
                )

                img_paths = document.metadata.get("images", [])
                await self.save_images(
                    chunk_id=chunk.id,
                    img_paths=img_paths,
                    session=uow.session,
                    user_id=user_id,
                )
                return chunk
        except HTTPException:
            raise
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Chunk 저장 중 오류: {e}",
            ) from e

    async def save_images(
        self,
        chunk_id: str,
        img_paths: List[str],
        user_id: str,
        *,
        session: AsyncIOMotorClientSession,
    ) -> None:
        for img_path in img_paths:
            await self.image_repository.create(
                Image(chunk_id=chunk_id, image_path=img_path, creator=user_id),
                session=session,
            )
