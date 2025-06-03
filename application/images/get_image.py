from typing import List

from fastapi import HTTPException, status
from application.services.validator import Validator
from domain.images.models import Image


class GetImage:
    def __init__(
        self,
        validator: Validator,
    ):
        self.validator = validator

    async def __call__(self, image_id: str, user_id: str) -> Image:
        try:
            image = await self.validator.image_validator(image_id, user_id)
            return image
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
