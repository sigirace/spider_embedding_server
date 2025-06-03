from fastapi import HTTPException, status
from domain.apps.models import App
from domain.apps.repository import IAppRepository


class CreateApp:
    def __init__(
        self,
        app_repository: IAppRepository,
    ):
        self.app_repository = app_repository

    async def __call__(
        self,
        app: App,
    ) -> App:
        try:

            if await self.app_repository.duplicate_check(
                creator=app.creator,
                app_name=app.app_name,
            ):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="이미 사용자가 동일한 이름의 App을 가지고 있습니다.",
                )

            app.id = await self.app_repository.create(app)
            return app
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
