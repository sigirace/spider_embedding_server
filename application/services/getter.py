from typing import List
from itertools import chain
import asyncio

from domain.apps.models import App
from domain.apps.repository import IAppRepository
from domain.chunks.models import Chunk
from domain.chunks.repository import IChunkRepository
from domain.documents.models import Document
from domain.documents.repository import IDocumentRepository
from domain.images.models import Image
from domain.images.repository import IImageRepository


class Getter:
    def __init__(
        self,
        app_repository: IAppRepository,
        document_repository: IDocumentRepository,
        chunk_repository: IChunkRepository,
        image_repository: IImageRepository,
    ):
        self.app_repository = app_repository
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.image_repository = image_repository

    async def get_image_by_chunk(self, chunk: Chunk) -> List[Image]:
        return await self.image_repository.get_by_chunk_id(chunk.id)

    async def get_chunk_by_document(self, document: Document) -> List[Chunk]:
        return await self.chunk_repository.get_by_document_id(document.id)

    async def get_image_by_document(self, document: Document) -> List[Image]:
        chunks = await self.get_chunk_by_document(document)
        image_lists = await asyncio.gather(
            *(self.get_image_by_chunk(chunk) for chunk in chunks)
        )
        return list(chain.from_iterable(image_lists))

    async def get_document_by_app(self, app: App) -> List[Document]:
        return await self.document_repository.list_by_app_id(app.id)

    async def get_chunk_by_app(self, app: App) -> List[Chunk]:
        documents = await self.get_document_by_app(app)
        chunk_lists = await asyncio.gather(
            *(self.get_chunk_by_document(doc) for doc in documents)
        )
        return list(chain.from_iterable(chunk_lists))

    async def get_image_by_app(self, app: App) -> List[Image]:
        chunks = await self.get_chunk_by_app(app)
        image_lists = await asyncio.gather(
            *(self.get_image_by_chunk(chunk) for chunk in chunks)
        )
        return list(chain.from_iterable(image_lists))
