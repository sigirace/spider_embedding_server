from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class EmbedModelType(str, Enum):
    KURE = "kure"
    NOMIC = "nomic"


class EmbedRequest(BaseModel):
    model_type: EmbedModelType = Field(
        default=EmbedModelType.KURE,
        description="임베딩 모델 타입",
    )
