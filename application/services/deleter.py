from typing import Callable

from application.services.getter import Getter
from common.uow import MongoUnitOfWork
from domain.apps.models import App
from domain.apps.repository import IAppRepository
from domain.chunks.models import Chunk
from domain.chunks.repository import IChunkRepository
from domain.documents.models import Document
from domain.documents.repository import IDocumentRepository
from domain.embeddings.models import Embedding
from domain.embeddings.repository import IEmbedRepository
from domain.images.models import Image
from domain.images.repository import IImageRepository
from domain.vectors.repository import IVectorStoreRepository
from infra.service.file_storage_service import LocalFileStorageService
from utils.object_utils import get_str_id


class Deleter:

    def __init__(
        self,
        app_repository: IAppRepository,
        document_repository: IDocumentRepository,
        chunk_repository: IChunkRepository,
        image_repository: IImageRepository,
        embed_repository: IEmbedRepository,
        vector_store_factory: Callable[[str], IVectorStoreRepository],
        file_storage_service: LocalFileStorageService,
        uow_factory: Callable[[], MongoUnitOfWork],
        getter: Getter,
    ):
        self.app_repository = app_repository
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.image_repository = image_repository
        self.embed_repository = embed_repository
        self.vector_store_factory = vector_store_factory
        self.fs = file_storage_service
        self._uow_factory = uow_factory
        self.getter = getter

    async def delete_embed(self, embedding: Embedding, session=None):

        store = self.vector_store_factory(embedding.collection_name)

        async with self._uow_factory() as uow:

            if not session:
                session = uow.session

            await store.delete(ids=[embedding.embed_pk])
            await self.embed_repository.delete(
                embed_id=embedding.id,
                session=session,
            )

    async def delete_image(self, image: Image, session=None):
        async with self._uow_factory() as uow:

            if not session:
                session = uow.session

            await self.image_repository.delete(
                image_id=image.id,
                session=session,
            )
            await self.fs.delete_file(image.image_path)

    async def delete_chunk(self, chunk: Chunk, session=None):
        async with self._uow_factory() as uow:
            if not session:
                session = uow.session

            embedding_list = await self.getter.get_embeddings_by_chunk(chunk)

            for embedding in embedding_list:
                await self.delete_embed(
                    embedding=embedding,
                    session=session,
                )

            image_list = await self.getter.get_image_by_chunk(chunk=chunk)

            for image in image_list:
                await self.delete_image(
                    image=image,
                    session=session,
                )

            await self.chunk_repository.delete(
                chunk_id=chunk.id,
                session=session,
            )

    async def delete_document(self, document: Document, session=None):
        async with self._uow_factory() as uow:
            if not session:
                session = uow.session

            chunk_list = await self.getter.get_chunk_by_document(document)

            for chunk in chunk_list:
                await self.delete_chunk(
                    chunk=chunk,
                    session=session,
                )

            await self.document_repository.delete(
                document_id=document.id,
                session=session,
            )

            await self.fs.delete_file(document.file_path)

    async def delete_app(self, app: App, user_id: str, session=None):
        collection_name = f"{user_id}_{app.app_name}"
        store = self.vector_store_factory(collection_name)

        async with self._uow_factory() as uow:
            if not session:
                session = uow.session

            document_list = await self.getter.get_document_by_app(app)

            for document in document_list:
                await self.delete_document(
                    document=document,
                    session=session,
                )

            await self.app_repository.delete(
                app_id=app.id,
                session=session,
            )

            await store.drop()

        await self.fs.delete_folder(folder_name=get_str_id(app.id))
