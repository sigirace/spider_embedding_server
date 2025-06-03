from datetime import UTC, datetime

from fastapi import HTTPException, status
from application.services.generator import Generator
from application.services.validator import Validator
from domain.images.models import Image
from domain.images.repository import IImageRepository


class ImageGenerator:
    def __init__(
        self,
        image_repository: IImageRepository,
        generator: Generator,
        validator: Validator,
    ):
        self.image_repository = image_repository
        self.generator = generator
        self.validator = validator

    async def __call__(
        self,
        image_id: str,
        user_id: str,
    ) -> Image:
        try:
            image = await self.validator.image_validator(
                image_id=image_id,
                user_id=user_id,
            )

            description = await self.generator.generate_image_description(
                image=image,
            )

            image.image_description = description
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
