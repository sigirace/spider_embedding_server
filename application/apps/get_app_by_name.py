from fastapi import HTTPException, status
from application.services.validator import Validator
from domain.apps.models import App
from domain.apps.repository import IAppRepository


class GetAppByName:
    def __init__(
        self,
        validator: Validator,
    ):
        self.validator = validator

    async def __call__(self, app_name: str, user_id: str) -> App:

        app = await self.validator.app_name_validator(
            app_name=app_name,
            user_id=user_id,
        )

        return app
