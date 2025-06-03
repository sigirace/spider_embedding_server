from datetime import UTC, datetime
from typing import List, Tuple

from application.services.generator import Generator
from application.services.getter import Getter
from application.services.validator import Validator
from domain.images.repository import IImageRepository
from domain.llms.models import ChunkGeneratorError, ImageGeneratorError
from utils.object_utils import get_str_id


class ChunkListGenerator:
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
        chunk_id_list: List[str],
        user_id: str,
    ) -> Tuple[
        List[str], List[str], List[ImageGeneratorError], List[ChunkGeneratorError]
    ]:
        success_image_list = []
        success_chunk_list = []
        failed_image_list: List[ImageGeneratorError] = []
        failed_chunk_list: List[ChunkGeneratorError] = []

        for chunk_id in chunk_id_list:
            try:
                chunk = await self.validator.chunk_validator(
                    chunk_id=chunk_id, user_id=user_id
                )
                image_list = await self.getter.get_image_by_chunk(chunk)

                if not image_list:
                    continue

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
                        failed_image_list.append(
                            ImageGeneratorError(
                                image_id=get_str_id(image.id),
                                error=str(e),
                            )
                        )

                success_chunk_list.append(chunk_id)

            except Exception as e:
                failed_chunk_list.append(
                    ChunkGeneratorError(
                        chunk_id=chunk_id,
                        error=str(e),
                    ),
                )

        return (
            success_image_list,
            success_chunk_list,
            failed_image_list,
            failed_chunk_list,
        )
