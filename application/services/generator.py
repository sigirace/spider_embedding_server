from fastapi import HTTPException, status
from domain.images.models import Image
from domain.images.repository import IImageRepository
from domain.llms.api_repository import ILlmAPIRepository


class Generator:
    def __init__(
        self,
        llm_repository: ILlmAPIRepository,
        image_repository: IImageRepository,
    ):
        self.llm_repository = llm_repository
        self.image_repository = image_repository

    async def generate_image_description(
        self,
        image: Image,
    ) -> str:
        if image.image_description:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="이미지 설명이 이미 존재합니다.",
            )
        return await self.llm_repository.describe_image(f"./{image.image_path}")
