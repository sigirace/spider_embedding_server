from fastapi import HTTPException, status
from domain.apps.models import App
from domain.apps.repository import IAppRepository
from domain.chunks.models import Chunk
from domain.chunks.repository import IChunkRepository
from domain.documents.models import Document
from domain.documents.repository import IDocumentRepository
from domain.embeddings.repository import IEmbedRepository
from domain.images.models import Image
from domain.images.repository import IImageRepository
from utils.object_utils import get_object_id


class Validator:

    def __init__(
        self,
        app_repository: IAppRepository,
        document_repository: IDocumentRepository,
        chunk_repository: IChunkRepository,
        image_repository: IImageRepository,
        embed_repository: IEmbedRepository,
    ):
        self.document_repository = document_repository
        self.app_repository = app_repository
        self.chunk_repository = chunk_repository
        self.image_repository = image_repository
        self.embed_repository = embed_repository

    async def app_validator(
        self,
        app_id: str,
        user_id: str,
    ) -> App:

        oid = get_object_id(app_id)
        app = await self.app_repository.get(oid)

        if not app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="앱을 찾을 수 없습니다.",
            )

        if app.creator != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="권한이 없습니다.",
            )

        return app

    async def app_name_validator(
        self,
        app_name: str,
        user_id: str,
    ) -> App:
        app = await self.app_repository.get_by_name(
            app_name=app_name,
            creator=user_id,
        )
        if not app:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"{app_name} 이름으로 앱을 찾을 수 없습니다.",
            )

        return app

    async def document_validator(
        self,
        document_id: str,
        user_id: str,
    ) -> Document:

        oid = get_object_id(document_id)
        document = await self.document_repository.get(oid)

        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="문서를 찾을 수 없습니다.",
            )

        if document.creator != user_id:
            await self.app_validator(document.app_id, user_id)

        return document

    async def chunk_validator(
        self,
        chunk_id: str,
        user_id: str,
    ) -> Chunk:

        oid = get_object_id(chunk_id)
        chunk = await self.chunk_repository.get(oid)

        if not chunk:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="청크를 찾을 수 없습니다.",
            )

        if chunk.creator != user_id:
            await self.document_validator(chunk.document_id, user_id)

        return chunk

    async def image_validator(
        self,
        image_id: str,
        user_id: str,
    ) -> Image:
        oid = get_object_id(image_id)
        image = await self.image_repository.get(oid)

        if not image:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="이미지를 찾을 수 없습니다.",
            )

        if image.creator != user_id:
            await self.chunk_validator(image.chunk_id, user_id)

        return image

    async def embed_validator(
        self,
        embed_id: str,
        user_id: str,
    ):
        oid = get_object_id(embed_id)
        embedding = await self.embed_repository.get(oid)

        if not embedding:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Embedding을 찾을 수 없습니다.",
            )

        if embedding.creator != user_id:
            await self.chunk_validator(chunk_id=embedding.chunk_id, user_id=user_id)

        return embedding
