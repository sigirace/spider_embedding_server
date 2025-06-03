from domain.images.models import Image, ImageUpdate
from interface.dto.image_dto import ImageResponse, ImageUpdateRequest


class ImageMapper:
    @staticmethod
    def to_response(image: Image) -> ImageResponse:
        return ImageResponse(
            id=str(image.id),
            chunk_id=str(image.chunk_id),
            image_path=image.image_path,
            image_description=image.image_description,
        )

    @staticmethod
    def to_update(request: ImageUpdateRequest) -> ImageUpdate:
        return ImageUpdate(
            image_description=request.image_description,
        )
