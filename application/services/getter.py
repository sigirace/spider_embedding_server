from typing import List
from itertools import chain
import asyncio

from bson import ObjectId

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
from utils.object_utils import get_str_id


class Getter:
    def __init__(
        self,
        app_repository: IAppRepository,
        document_repository: IDocumentRepository,
        chunk_repository: IChunkRepository,
        image_repository: IImageRepository,
        embed_repository: IEmbedRepository,
    ):
        self.app_repository = app_repository
        self.document_repository = document_repository
        self.chunk_repository = chunk_repository
        self.image_repository = image_repository
        self.embed_repository = embed_repository

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

    async def get_app_by_chunk(self, chunk: Chunk) -> App:
        document = await self.document_repository.get(chunk.document_id)
        app = await self.app_repository.get(document.app_id)
        return app

    async def get_app_by_image(self, image: Image) -> App:
        chunk = await self.chunk_repository.get(image.chunk_id)
        return await self.get_app_by_chunk(chunk)

    async def get_app_by_document(self, document: Document) -> App:
        return await self.app_repository.get(document.app_id)

    async def get_embeddings_by_chunk(self, chunk: Chunk) -> Embedding | None:
        return await self.embed_repository.get_by_chunk_id(chunk.id)

    async def get_embedding_by_document(self, document: Document) -> Embedding | None:
        chunks = await self.get_chunk_by_document(document)
        embedding_lists = await asyncio.gather(
            *(self.get_embeddings_by_chunk(chunk) for chunk in chunks)
        )
        return list(chain.from_iterable(embedding_lists))
