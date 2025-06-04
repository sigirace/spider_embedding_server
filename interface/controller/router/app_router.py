from typing import List

from dependency_injector.wiring import Provide, inject
from fastapi import APIRouter, Depends

from application.apps.create_app import CreateApp
from application.apps.delete_app import DeleteApp
from application.apps.get_app import GetApp
from application.apps.get_app_list import GetAppList
from application.apps.update_app import UpdateApp
from common.log_wrapper import log_request
from containers import Container
from domain.users.models import User
from interface.controller.dependency.auth import get_current_user
from interface.dto.app_dto import AppCreateRequest, AppResponse, AppUpdateRequest
from interface.mapper.app_mapper import AppMapper

router = APIRouter(prefix="/app")


@router.post("/", response_model=AppResponse)
@log_request()
@inject
async def create_app(
    request: AppCreateRequest,
    user: User = Depends(get_current_user),
    create_app: CreateApp = Depends(Provide[Container.create_app]),
):
    app = AppMapper.to_domain(user.user_id, request)
    created_app = await create_app(app)
    return AppMapper.to_response(created_app)


@router.get("/list", response_model=List[AppResponse])
@log_request()
@inject
async def get_app_list(
    user: User = Depends(get_current_user),
    get_app_list: GetAppList = Depends(Provide[Container.get_app_list]),
):
    apps = await get_app_list(user.user_id)
    return [AppMapper.to_response(app) for app in apps]


@router.get("/{app_id}", response_model=AppResponse)
@log_request()
@inject
async def get_app(
    app_id: str,
    user: User = Depends(get_current_user),
    get_app: GetApp = Depends(Provide[Container.get_app]),
):
    app = await get_app(app_id, user.user_id)
    return AppMapper.to_response(app)


@router.put("/{app_id}", response_model=AppResponse)
@log_request()
@inject
async def update_app(
    app_id: str,
    request: AppUpdateRequest,
    user: User = Depends(get_current_user),
    update_app: UpdateApp = Depends(Provide[Container.update_app]),
):
    app = AppMapper.to_update_domain(request)
    updated_app = await update_app(
        app_id=app_id,
        app=app,
        user_id=user.user_id,
    )
    return AppMapper.to_response(updated_app)


@router.delete("/{app_id}")
@log_request()
@inject
async def delete_app(
    app_id: str,
    user: User = Depends(get_current_user),
    delete_app: DeleteApp = Depends(Provide[Container.delete_app]),
):
    await delete_app(app_id, user.user_id)

    return {"message": f"{app_id} App Deleted"}
