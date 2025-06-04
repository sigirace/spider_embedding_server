from fastapi import HTTPException, status
from application.services.deleter import Deleter
from application.services.validator import Validator


class DeleteDocument:
    def __init__(
        self,
        deleter: Deleter,
        validator: Validator,
    ):
        self.deleter = deleter
        self.validator = validator

    async def __call__(
        self,
        document_id: str,
        user_id: str,
    ):
        try:
            document = await self.validator.document_validator(
                document_id,
                user_id,
            )

            await self.deleter.delete_document(document)

        except HTTPException as e:
            raise e
        except Exception as e:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"Failed to delete document: {e}",
            )
