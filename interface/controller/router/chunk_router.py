from typing import List
from fastapi import APIRouter, Depends

from application.chunks.create_chunk import CreateChunk
from application.chunks.get_chunk import GetChunk
from application.chunks.get_chunk_list import GetChunkList
from application.chunks.update_chunk import UpdateChunk
from common.log_wrapper import log_request
from containers import Container
from domain.users.models import User
from interface.controller.dependency.auth import get_current_user
from interface.dto.chunk_dto import (
    ChunkDetailResponse,
    ChunkErrorResponse,
    ChunkListRequest,
    ChunkListResponse,
    ChunkResponse,
    ChunkRequest,
    ChunkUpdateRequest,
)
from dependency_injector.wiring import inject, Provide

from interface.mapper.chunk_mapper import ChunkMapper

router = APIRouter(prefix="/chunk")


@router.post("/list", response_model=ChunkListResponse)
@log_request()
@inject
async def get_chunk_list(
    request: ChunkListRequest,
    user: User = Depends(get_current_user),
    create_chunk: CreateChunk = Depends(Provide[Container.create_chunk]),
):
    success_list: List[str] = []
    error_list: List[ChunkErrorResponse] = []

    for document_id in request.document_id:
        try:
            chunk_request = ChunkMapper.to_domain(request, document_id)
            chunk_list = await create_chunk(chunk_request, user.user_id)
            if chunk_list:
                success_list.append(document_id)
        except Exception as e:
            error_list.append(
                ChunkErrorResponse(
                    document_id=document_id,
                    error_message=str(e),
                )
            )

    return ChunkListResponse(
        success_list=success_list,
        error_list=error_list,
    )


@router.post("/{document_id}", response_model=List[ChunkResponse])
@log_request()
@inject
async def create_chunk(
    document_id: str,
    request: ChunkRequest,
    user: User = Depends(get_current_user),
    create_chunk: CreateChunk = Depends(Provide[Container.create_chunk]),
):
    chunk_request = ChunkMapper.to_domain(request, document_id)
    chunk_list = await create_chunk(chunk_request, user.user_id)
    return [ChunkMapper.to_response(chunk) for chunk in chunk_list]


@router.get("/{chunk_id}", response_model=ChunkDetailResponse)
@log_request()
@inject
async def get_chunk(
    chunk_id: str,
    user: User = Depends(get_current_user),
    get_chunk: GetChunk = Depends(Provide[Container.get_chunk]),
):
    chunk_detail_response = await get_chunk(chunk_id, user.user_id)
    return ChunkMapper.to_detail_response(chunk_detail_response)


@router.get("/list/{document_id}", response_model=List[ChunkResponse])
@log_request()
@inject
async def get_chunk_list(
    document_id: str,
    user: User = Depends(get_current_user),
    get_chunk_list: GetChunkList = Depends(Provide[Container.get_chunk_list]),
):
    chunks = await get_chunk_list(document_id, user.user_id)
    return [ChunkMapper.to_response(chunk) for chunk in chunks]


@router.put("/{chunk_id}", response_model=ChunkDetailResponse)
@log_request()
@inject
async def update_chunk(
    chunk_id: str,
    request: ChunkUpdateRequest,
    user: User = Depends(get_current_user),
    update_chunk: UpdateChunk = Depends(Provide[Container.update_chunk]),
):
    chunk_update_request = ChunkMapper.to_update_domain(request)
    updated_chunk_detail = await update_chunk(
        chunk_id=chunk_id,
        request=chunk_update_request,
        user_id=user.user_id,
    )
    return ChunkMapper.to_detail_response(updated_chunk_detail)
