from datetime import UTC, datetime
from typing import List, Tuple

from fastapi import HTTPException, status

from application.services.generator import Generator
from application.services.getter import Getter
from application.services.validator import Validator
from domain.images.models import Image
from domain.images.repository import IImageRepository
from domain.llms.models import ImageGeneratorError
from utils.object_utils import get_str_id


class AppGenerator:
    def __init__(
        self,
        image_repository: IImageRepository,
        generator: Generator,
        validator: Validator,
        getter: Getter,
    ):
        self.image_repository = image_repository
        self.generator = generator
        self.validator = validator
        self.getter = getter

    async def __call__(
        self,
        app_id: str,
        user_id: str,
    ) -> Tuple[List[str], List[ImageGeneratorError]]:
        success_image_list = []
        failed: List[ImageGeneratorError] = []

        try:
            app = await self.validator.app_validator(
                app_id=app_id,
                user_id=user_id,
            )
            image_list = await self.getter.get_image_by_app(app)

            if not image_list:
                return success_image_list, failed

            for image in image_list:
                try:
                    description = await self.generator.generate_image_description(
                        image=image,
                    )
                    image.image_description = description
                    image.updater = user_id
                    image.updated_at = datetime.now(UTC)
                    await self.image_repository.update(image)
                    success_image_list.append(get_str_id(image.id))

                except Exception as e:
                    failed.append(
                        ImageGeneratorError(
                            image_id=get_str_id(image.id),
                            error=str(e),
                        )
                    )

            return success_image_list, failed

        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
