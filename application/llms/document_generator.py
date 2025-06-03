from datetime import UTC, datetime
from typing import List, Tuple

from fastapi import HTTPException, status

from application.services.generator import Generator
from application.services.getter import Getter
from application.services.validator import Validator
from domain.images.models import Image
from domain.images.repository import IImageRepository
from domain.llms.models import DocumentGeneratorError, ImageGeneratorError
from utils.object_utils import get_str_id


class DocumentListGenerator:
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
        document_id_list: List[str],
        user_id: str,
    ) -> Tuple[
        List[str], List[str], List[ImageGeneratorError], List[DocumentGeneratorError]
    ]:
        success_image_list = []
        success_document_list = []
        failed_image_list: List[ImageGeneratorError] = []
        failed_document_list: List[DocumentGeneratorError] = []

        for document_id in document_id_list:
            try:
                document = await self.validator.document_validator(
                    document_id=document_id,
                    user_id=user_id,
                )
                image_list = await self.getter.get_image_by_document(document)

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

                success_document_list.append(document_id)

            except Exception as e:
                failed_document_list.append(
                    DocumentGeneratorError(
                        document_id=document_id,
                        error=str(e),
                    ),
                )

        return (
            success_image_list,
            success_document_list,
            failed_image_list,
            failed_document_list,
        )
