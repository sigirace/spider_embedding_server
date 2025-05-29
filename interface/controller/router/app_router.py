from fastapi import APIRouter, Depends, HTTPException
from dependency_injector.wiring import inject, Provide

from common.exception import InternalServerError
from common.system_logger import SystemLogger
from containers import Container
from domain.users.models import User
from interface.controller.dependency.auth import get_current_user

router = APIRouter(prefix="/app")


@router.get("/")
@inject
async def hello(
    # user: User = Depends(get_current_user),
    logger: SystemLogger = Depends(Provide[Container.system_logger]),
):

    await logger.info("Started sample endpoint")
    await logger.info("Completed sample endpoint")
    await logger.error("Error!!!!!!")
    return {"data": f"good"}
