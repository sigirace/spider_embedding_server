from fastapi import APIRouter, Depends

from application.embeddings.app_embedding import AppEmbedding
from application.embeddings.chunk_embedding import ChunkEmbedding
from application.embeddings.delete_embedding import DeleteEmbedding
from application.embeddings.document_embedding import DocumentEmbedding
from application.embeddings.search_embedding import SearchEmbedding
from common.log_wrapper import log_request
from domain.users.models import User
from interface.controller.dependency.auth import get_current_user
from containers import Container
from dependency_injector.wiring import Provide, inject

from interface.dto.embedding_dto import EmbedRequest, SearchRequest
from interface.mapper.embedding_maaper import EmbeddingMapper

router = APIRouter(prefix="/embedding")


@router.post("/chunk/{chunk_id}")
@log_request()
@inject
async def chunk_embedding(
    chunk_id: str,
    embed_request: EmbedRequest,
    user: User = Depends(get_current_user),
    chunk_embedding: ChunkEmbedding = Depends(Provide[Container.chunk_embedding]),
):
    await chunk_embedding(
        chunk_id=chunk_id,
        model_type=embed_request.model_type.value,
        user_id=user.user_id,
    )
    return {"message": "Chunk embedding completed"}


@router.post("/document/{document_id}")
@log_request()
@inject
async def document_embedding(
    document_id: str,
    embed_request: EmbedRequest,
    user: User = Depends(get_current_user),
    document_embedding: DocumentEmbedding = Depends(
        Provide[Container.document_embedding]
    ),
):
    success_list, error_list = await document_embedding(
        document_id=document_id,
        model_type=embed_request.model_type.value,
        user_id=user.user_id,
    )

    return {
        "success_list": success_list,
        "error_list": error_list,
    }


@router.post("/app/{app_id}")
@log_request()
@inject
async def app_embedding(
    app_id: str,
    embed_request: EmbedRequest,
    user: User = Depends(get_current_user),
    app_embedding: AppEmbedding = Depends(Provide[Container.app_embedding]),
):
    success_list, error_list = await app_embedding(
        app_id=app_id,
        model_type=embed_request.model_type.value,
        user_id=user.user_id,
    )

    return {
        "success_list": success_list,
        "error_list": error_list,
    }


@router.delete("/embed/{embed_id}")
@log_request()
@inject
async def delete_chunk_embedding(
    embed_id: str,
    user: User = Depends(get_current_user),
    delete_embedding: DeleteEmbedding = Depends(Provide[Container.delete_embedding]),
):
    await delete_embedding(embed_id, user.user_id)

    return {"message": f"{embed_id} Embedding Deleted"}


@router.post("/search")
@log_request()
@inject
async def search_embedding(
    search_request: SearchRequest,
    user: User = Depends(get_current_user),
    search_embedding: SearchEmbedding = Depends(Provide[Container.search_embedding]),
):
    search_embedding_schema = EmbeddingMapper.to_request(
        search_request=search_request,
        user_id=user.user_id,
    )
    search_result_list = await search_embedding(
        search_embedding_schema=search_embedding_schema
    )
    search_response_list = EmbeddingMapper.to_response(search_result_list)

    return search_response_list
