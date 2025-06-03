from datetime import UTC, datetime
from typing import List, Tuple

from fastapi import HTTPException, status

from application.services.generator import Generator
from application.services.getter import Getter
from application.services.validator import Validator
from domain.images.models import Image
from domain.images.repository import IImageRepository
from domain.llms.models import ImageGeneratorError


class ImageListGenerator:
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
        image_id_list: List[str],
        user_id: str,
    ) -> Tuple[List[str], List[ImageGeneratorError]]:
        success = []
        failed: List[ImageGeneratorError] = []

        for image_id in image_id_list:
            try:
                # 이미지 유효성 검증
                image = await self.validator.image_validator(
                    image_id=image_id,
                    user_id=user_id,
                )

                # 이미지 설명 생성
                description = await self.generator.generate_image_description(
                    image=image,
                )

                # 필드 업데이트
                image.image_description = description
                image.updater = user_id
                image.updated_at = datetime.now(UTC)

                # DB 반영
                await self.image_repository.update(image)
                success.append(image_id)
            except Exception as e:
                failed.append(
                    ImageGeneratorError(
                        image_id=image_id,
                        error=str(e),
                    )
                )

        return success, failed
