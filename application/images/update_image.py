from datetime import UTC, datetime
from fastapi import HTTPException, status
from application.services.validator import Validator
from domain.images.models import ImageUpdate
from domain.images.repository import IImageRepository


class UpdateImage:
    def __init__(self, image_repository: IImageRepository, validator: Validator):
        self.image_repository = image_repository
        self.validator = validator

    async def __call__(
        self,
        image_id: str,
        request: ImageUpdate,
        user_id: str,
    ):
        try:
            image = await self.validator.image_validator(image_id, user_id)
            image.image_description = request.image_description
            image.updater = user_id
            image.updated_at = datetime.now(UTC)
            await self.image_repository.update(image)
            return image
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
