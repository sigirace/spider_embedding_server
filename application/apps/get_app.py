from fastapi import HTTPException
from application.services.validator import Validator
from domain.apps.models import App


class GetApp:
    def __init__(
        self,
        validator: Validator,
    ):
        self.validator = validator

    async def __call__(
        self,
        app_id: str,
        user_id: str,
    ) -> App:
        try:
            return await self.validator.app_validator(
                app_id=app_id,
                user_id=user_id,
            )
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=str(e),
            )
