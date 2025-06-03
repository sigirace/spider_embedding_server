from datetime import UTC, datetime
from bson import ObjectId
from fastapi import HTTPException, status
from application.services.validator import Validator
from domain.apps.models import App
from domain.apps.repository import IAppRepository


class UpdateApp:
    def __init__(
        self,
        app_repository: IAppRepository,
        validator: Validator,
    ):
        self.app_repository = app_repository
        self.validator = validator

    async def __call__(
        self,
        app_id: str,
        app: App,
    ) -> App:
        try:
            existing_app = await self.validator.app_validator(
                app_id=app_id,
                user_id=app.creator,
            )

            if existing_app.app_name != app.app_name:
                await self.app_repository.duplicate_check(
                    creator=app.creator,
                    app_name=app.app_name,
                )

            existing_app.updater = app.creator
            existing_app.updated_at = datetime.now(UTC)
            await self.app_repository.update(existing_app.id, app)

            return app

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
