from typing import List

from fastapi import HTTPException, status
from application.services.validator import Validator
from domain.images.models import Image
from domain.images.repository import IImageRepository


class GetImageList:
    def __init__(
        self,
        image_repository: IImageRepository,
        validator: Validator,
    ):
        self.image_repository = image_repository
        self.validator = validator

    async def __call__(self, chunk_id: str, user_id: str) -> List[Image]:
        try:
            chunk = await self.validator.chunk_validator(chunk_id, user_id)
            image_list = await self.image_repository.get_by_chunk_id(chunk.id)
            return image_list
        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=str(e),
            )
