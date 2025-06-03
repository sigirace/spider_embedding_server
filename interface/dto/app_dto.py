from typing import List

from pydantic import BaseModel, Field

from common.models import LifeCycle


class AppRequest(BaseModel):
    app_name: str = Field(..., description="앱 이름")
    description: str | None = Field(None, description="앱 설명")
    keywords: List[str] = Field(default=[], description="앱 키워드")


class AppResponse(LifeCycle, AppRequest):
    id: str = Field(..., description="앱 ID")
