from fastapi import HTTPException, status
from application.services.embedder import Embedder
from application.services.getter import Getter
from application.services.validator import Validator
from domain.embeddings.models import EmbedSchema


class ChunkEmbedding:
    def __init__(
        self,
        validator: Validator,
        getter: Getter,
        embedder: Embedder,
    ):
        self.validator = validator
        self.getter = getter
        self.embedder = embedder

    async def __call__(
        self,
        chunk_id: str,
        model_type: str,
        user_id: str,
    ):
        chunk = await self.validator.chunk_validator(chunk_id, user_id)

        if chunk.embeded_state:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="이미 임베딩을 수행한 청크입니다.",
            )

        images = await self.getter.get_image_by_chunk(chunk)
        app = await self.getter.get_app_by_chunk(chunk)
        existing_embeddings = await self.getter.get_embeddings_by_chunk(chunk)

        if existing_embeddings:
            await self.embedder.delete_existing_embeddings(
                collection_name=f"{user_id}_{app.app_name}",
                ids=existing_embeddings.embed_pk,
                embed_id=existing_embeddings.id,
                chunk=chunk,
            )

        schema = EmbedSchema(
            text=chunk.content,
            image_descriptions=[
                img.image_description for img in images if img.image_description
            ],
        )

        await self.embedder.execute(
            chunk=chunk,
            embed_schema=schema,
            model_type=model_type,
            user_id=user_id,
            collection_name=f"{user_id}_{app.app_name}",
        )
