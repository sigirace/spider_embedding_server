from dependency_injector import containers, providers
from application.chunks.get_chunk import GetChunk
from application.chunks.get_chunk_list import GetChunkList
from application.chunks.update_chunk import UpdateChunk
from application.images.get_image import GetImage
from application.images.get_image_list import GetImageList
from application.images.update_image import UpdateImage
from application.llms.app_generator import AppGenerator
from application.llms.chunk_generator import ChunkListGenerator
from application.llms.document_generator import DocumentListGenerator
from application.llms.image_generator import ImageGenerator
from application.llms.image_list_generator import ImageListGenerator
from application.services.generator import Generator
from application.services.getter import Getter
from database.mongo import get_async_mongo_client, get_async_mongo_database
from common.uow import MongoUnitOfWork
from common.system_logger import SystemLogger
from infra.api.haiqv_ollama import HaiqvOllamaLLM
from infra.implement.llm_repository_impl import LlmRepositoryImpl
from infra.service.file_storage_service import LocalFileStorageService
from infra.implement.app_repository_impl import AppRepositoryImpl
from infra.implement.document_repository_impl import DocumentRepositoryImpl
from infra.implement.chunk_repository_impl import ChunkRepositoryImpl
from infra.implement.image_repository_impl import ImageRepositoryImpl
from application.services.validator import Validator
from application.services.chunker import Chunker
from application.apps.create_app import CreateApp
from application.apps.get_app import GetApp
from application.apps.get_app_list import GetAppList
from application.apps.update_app import UpdateApp
from application.documents.create_document import CreateDocument
from application.documents.get_document import GetDocument
from application.documents.get_document_list import GetDocumentList
from application.documents.update_document import UpdateDocument
from application.chunks.create_chunk import CreateChunk
from application.users.token_service import TokenService


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        packages=[
            "interface.controller.dependency",
            "interface.controller.router",
            "middleware",
        ]
    )

    # database
    motor_client = providers.Singleton(get_async_mongo_client)
    motor_db = providers.Singleton(get_async_mongo_database, client=motor_client)
    _uow_provider = providers.Factory(MongoUnitOfWork, db=motor_db)
    uow_factory = _uow_provider.provider

    # logger
    system_logger = providers.Singleton(SystemLogger, db=motor_db)

    # api
    haiqv_ollama_llm = providers.Singleton(HaiqvOllamaLLM)

    # repository
    app_repository = providers.Factory(
        AppRepositoryImpl,
        db=motor_db,
    )
    document_repository = providers.Factory(
        DocumentRepositoryImpl,
        db=motor_db,
    )
    chunk_repository = providers.Factory(
        ChunkRepositoryImpl,
        db=motor_db,
    )
    image_repository = providers.Factory(
        ImageRepositoryImpl,
        db=motor_db,
    )
    llm_repository = providers.Factory(
        LlmRepositoryImpl,
        llm=haiqv_ollama_llm,
    )

    # service
    file_storage_service = providers.Singleton(
        LocalFileStorageService, base_dir="./static/data"
    )
    token_service = providers.Factory(TokenService)
    validator = providers.Factory(
        Validator,
        app_repository=app_repository,
        document_repository=document_repository,
        chunk_repository=chunk_repository,
        image_repository=image_repository,
    )
    chunker = providers.Factory(
        Chunker,
        chunk_repository=chunk_repository,
        image_repository=image_repository,
        file_storage_service=file_storage_service,
        uow_factory=uow_factory,
    )
    generator = providers.Factory(
        Generator,
        llm_repository=llm_repository,
        image_repository=image_repository,
    )
    getter = providers.Factory(
        Getter,
        image_repository=image_repository,
        chunk_repository=chunk_repository,
        document_repository=document_repository,
        app_repository=app_repository,
    )

    # app
    create_app = providers.Factory(
        CreateApp,
        app_repository=app_repository,
    )
    get_app = providers.Factory(
        GetApp,
        validator=validator,
    )
    get_app_list = providers.Factory(
        GetAppList,
        app_repository=app_repository,
    )
    update_app = providers.Factory(
        UpdateApp,
        app_repository=app_repository,
        validator=validator,
    )

    # document
    create_document = providers.Factory(
        CreateDocument,
        document_repository=document_repository,
        file_storage_service=file_storage_service,
        validator=validator,
    )
    get_document = providers.Factory(
        GetDocument, document_repository=document_repository, validator=validator
    )
    get_document_list = providers.Factory(
        GetDocumentList, document_repository=document_repository, validator=validator
    )
    update_document = providers.Factory(
        UpdateDocument,
        document_repository=document_repository,
        file_storage_service=file_storage_service,
        validator=validator,
    )

    # chunk
    create_chunk = providers.Factory(
        CreateChunk,
        chunk_repository=chunk_repository,
        file_storage_service=file_storage_service,
        chunker=chunker,
        validator=validator,
    )
    get_chunk = providers.Factory(
        GetChunk,
        validator=validator,
        chunker=chunker,
    )
    get_chunk_list = providers.Factory(
        GetChunkList,
        chunk_repository=chunk_repository,
        validator=validator,
    )
    update_chunk = providers.Factory(
        UpdateChunk,
        chunk_repository=chunk_repository,
        chunker=chunker,
        validator=validator,
    )

    # image
    get_image = providers.Factory(
        GetImage,
        validator=validator,
    )
    get_image_list = providers.Factory(
        GetImageList,
        image_repository=image_repository,
        validator=validator,
    )
    update_image = providers.Factory(
        UpdateImage,
        image_repository=image_repository,
        validator=validator,
    )

    # llm
    image_generator = providers.Factory(
        ImageGenerator,
        image_repository=image_repository,
        generator=generator,
        validator=validator,
    )
    image_list_generator = providers.Factory(
        ImageListGenerator,
        image_repository=image_repository,
        getter=getter,
        generator=generator,
        validator=validator,
    )
    chunk_list_generator = providers.Factory(
        ChunkListGenerator,
        image_repository=image_repository,
        getter=getter,
        generator=generator,
        validator=validator,
    )
    document_list_generator = providers.Factory(
        DocumentListGenerator,
        image_repository=image_repository,
        getter=getter,
        generator=generator,
        validator=validator,
    )
    app_generator = providers.Factory(
        AppGenerator,
        image_repository=image_repository,
        getter=getter,
        generator=generator,
        validator=validator,
    )
