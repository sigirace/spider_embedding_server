from typing import Optional
from pydantic import BaseModel


class ImageGeneratorError(BaseModel):
    image_id: Optional[str] = None
    error: str


class DocumentGeneratorError(BaseModel):
    document_id: str
    error: str


class ChunkGeneratorError(BaseModel):
    chunk_id: str
    error: str
