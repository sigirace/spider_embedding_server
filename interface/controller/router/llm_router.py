from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse


from application.llms.app_generator import AppGenerator
from application.llms.chunk_generator import ChunkListGenerator
from application.llms.document_generator import DocumentListGenerator
from application.llms.image_generator import ImageGenerator
from application.llms.image_list_generator import ImageListGenerator
from interface.controller.dependency.auth import get_current_user
from domain.users.models import User
from dependency_injector.wiring import inject, Provide
from common.log_wrapper import log_request

from typing import List
from containers import Container
from interface.dto.image_dto import ImageResponse
from interface.dto.llm_dto import (
    ChunkListResponseDTO,
    DocumentListResponseDTO,
    ImageListResponseDTO,
)
from interface.mapper.image_mapper import ImageMapper
from interface.mapper.llm_mapper import LlmMapper


router = APIRouter(prefix="/llm")


@router.post("/list/image", response_model=ImageListResponseDTO)
@log_request()
@inject
async def generate_image_list(
    image_id_list: List[str],
    image_list_generator: ImageListGenerator = Depends(
        Provide[Container.image_list_generator]
    ),
    user: User = Depends(get_current_user),
):
    image_list, failed = await image_list_generator(image_id_list, user.user_id)
    return LlmMapper.to_image_list_response(image_list, failed)


@router.post("/list/chunk", response_model=ChunkListResponseDTO)
@log_request()
@inject
async def generate_chunk_list(
    chunk_id_list: List[str],
    chunk_list_generator: ChunkListGenerator = Depends(
        Provide[Container.chunk_list_generator]
    ),
    user: User = Depends(get_current_user),
):
    image_list, chunk_list, failed_image_list, failed_chunk_list = (
        await chunk_list_generator(chunk_id_list, user.user_id)
    )
    return JSONResponse(
        content={
            "image_list": image_list,
            "chunk_list": chunk_list,
            "image_errors": [e.model_dump() for e in failed_image_list],
            "chunk_errors": [e.model_dump() for e in failed_chunk_list],
        }
    )


@router.post("/list/document", response_model=DocumentListResponseDTO)
@log_request()
@inject
async def generate_document_list(
    document_id_list: List[str],
    document_list_generator: DocumentListGenerator = Depends(
        Provide[Container.document_list_generator]
    ),
    user: User = Depends(get_current_user),
):
    (
        success_image_list,
        success_document_list,
        failed_image_list,
        failed_document_list,
    ) = await document_list_generator(document_id_list, user.user_id)
    return JSONResponse(
        content={
            "image_list": success_image_list,
            "document_list": success_document_list,
            "image_errors": [e.model_dump() for e in failed_image_list],
            "document_errors": [e.model_dump() for e in failed_document_list],
        }
    )


@router.post("/app/{app_id}", response_model=ImageListResponseDTO)
@log_request()
@inject
async def generate_app(
    app_id: str,
    app_generator: AppGenerator = Depends(Provide[Container.app_generator]),
    user: User = Depends(get_current_user),
):
    image_list, failed = await app_generator(app_id, user.user_id)
    return LlmMapper.to_image_list_response(image_list, failed)


@router.post("/{image_id}", response_model=ImageResponse)
@log_request()
@inject
async def generate_image(
    image_id: str,
    image_generator: ImageGenerator = Depends(Provide[Container.image_generator]),
    user: User = Depends(get_current_user),
):
    image = await image_generator(image_id, user.user_id)
    return ImageMapper.to_response(image)
