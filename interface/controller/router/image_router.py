import base64
import mimetypes
from fastapi import APIRouter, Depends
from fastapi.responses import FileResponse, JSONResponse
from application.images.get_image import GetImage
from application.images.update_image import UpdateImage
from interface.controller.dependency.auth import get_current_user
from domain.users.models import User
from dependency_injector.wiring import inject, Provide
from common.log_wrapper import log_request
from application.images.get_image_list import GetImageList
from domain.images.models import Image
from typing import List
from containers import Container
from interface.dto.image_dto import ImageResponse, ImageUpdateRequest
from interface.mapper.image_mapper import ImageMapper

router = APIRouter(prefix="/image")


@router.get("/{image_id}", response_model=ImageResponse)
@log_request()
@inject
async def get_image(
    image_id: str,
    user: User = Depends(get_current_user),
    get_image: GetImage = Depends(Provide[Container.get_image]),
):
    image = await get_image(image_id, user.user_id)
    return ImageMapper.to_response(image)


@router.get("/list/{chunk_id}", response_model=List[ImageResponse])
@log_request()
@inject
async def get_image_list(
    chunk_id: str,
    user: User = Depends(get_current_user),
    get_image_list: GetImageList = Depends(Provide[Container.get_image_list]),
):
    image_list = await get_image_list(chunk_id, user.user_id)
    return [ImageMapper.to_response(image) for image in image_list]


@router.put("/{image_id}", response_model=ImageResponse)
@log_request()
@inject
async def update_image(
    image_id: str,
    request: ImageUpdateRequest,
    user: User = Depends(get_current_user),
    update_image: UpdateImage = Depends(Provide[Container.update_image]),
):
    image_update_req = ImageMapper.to_update(request)
    image = await update_image(
        image_id=image_id,
        request=image_update_req,
        user_id=user.user_id,
    )
    return ImageMapper.to_response(image)


@router.get("/show/{image_id}", response_class=FileResponse)
@log_request()
@inject
async def show_image(
    image_id: str,
    get_image: GetImage = Depends(Provide[Container.get_image]),
    user: User = Depends(get_current_user),
):
    image = await get_image(
        image_id,
        user.user_id,
    )

    file_path = image.image_path
    mime_type, _ = mimetypes.guess_type(f"./{file_path}")
    return FileResponse(
        path=file_path,
        media_type=mime_type,
    )


@router.get("/show/base64/{image_id}", response_class=JSONResponse)
@log_request()
@inject
async def show_image_base64(
    image_id: str,
    get_image: GetImage = Depends(Provide[Container.get_image]),
    user: User = Depends(get_current_user),
):
    image = await get_image(image_id, user.user_id)
    file_path = image.image_path
    mime_type, _ = mimetypes.guess_type(f"./{file_path}")
    with open(file_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode("utf-8")
    data_url = f"data:{mime_type};base64,{encoded}"
    return JSONResponse(content={"data_url": data_url})
