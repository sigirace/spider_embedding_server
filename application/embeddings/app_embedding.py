from fastapi import HTTPException, status
from application.services.embedder import Embedder
from application.services.getter import Getter
from application.services.validator import Validator
from domain.embeddings.models import EmbedSchema
from utils.object_utils import get_str_id


class AppEmbedding:
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
        app_id: str,
        model_type: str,
        user_id: str,
    ):
        app = await self.validator.app_validator(app_id, user_id)
        chunk_list = await self.getter.get_chunk_by_app(app)

        success_list = []
        error_list = []

        for chunk in chunk_list:

            try:
                existing_embeddings = await self.getter.get_embeddings_by_chunk(chunk)

                if chunk.embeded_state and existing_embeddings:
                    success_list.append(
                        {
                            "chunk_id": get_str_id(chunk.id),
                            "embed_pk": existing_embeddings.embed_pk,
                        }
                    )
                    continue

                if existing_embeddings:
                    await self.embedder.delete_existing_embeddings(
                        collection_name=f"{user_id}_{app.app_name}",
                        ids=existing_embeddings.embed_pk,
                        embed_id=existing_embeddings.id,
                        chunk=chunk,
                    )

                images = await self.getter.get_image_by_chunk(chunk)

                schema = EmbedSchema(
                    text=chunk.content,
                    image_descriptions=[
                        img.image_description for img in images if img.image_description
                    ],
                )

                embed_pk = await self.embedder.execute(
                    chunk=chunk,
                    embed_schema=schema,
                    model_type=model_type,
                    user_id=user_id,
                    collection_name=f"{user_id}_{app.app_name}",
                )

                success_list.append(
                    {
                        "chunk_id": get_str_id(chunk.id),
                        "embed_pk": embed_pk,
                    }
                )
            except Exception as e:
                error_list.append(
                    {
                        "chunk_id": get_str_id(chunk.id),
                        "error": str(e),
                    }
                )
                continue

        return success_list, error_list
