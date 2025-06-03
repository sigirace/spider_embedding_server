from typing import List

from fastapi import HTTPException, status
from domain.apps.models import App
from domain.apps.repository import IAppRepository


class GetAppList:
    def __init__(self, app_repository: IAppRepository):
        self.app_repository = app_repository

    async def __call__(
        self,
        user_id: str,
    ) -> List[App]:
        try:
            apps = await self.app_repository.list_by_creator(user_id)
            if not apps:
                return []
            return apps
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
