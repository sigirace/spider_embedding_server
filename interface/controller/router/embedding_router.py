from fastapi import APIRouter, Depends

from application.embeddings.chunk_embedding import ChunkEmbedding
from common.log_wrapper import log_request
from domain.users.models import User
from interface.controller.dependency.auth import get_current_user
from containers import Container
from dependency_injector.wiring import Provide, inject

from interface.dto.embedding_dto import EmbedRequest

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
