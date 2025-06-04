from datetime import UTC, datetime
from bson import ObjectId
from fastapi import HTTPException, status
from application.services.validator import Validator
from domain.apps.models import App, AppUpdate
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
        app: AppUpdate,
        user_id: str,
    ) -> App:
        try:
            existing_app = await self.validator.app_validator(
                app_id=app_id,
                user_id=user_id,
            )

            existing_app.description = app.description
            existing_app.keywords = app.keywords
            existing_app.updater = user_id
            existing_app.updated_at = datetime.now(UTC)

            await self.app_repository.update(existing_app.id, existing_app)

            return existing_app

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
