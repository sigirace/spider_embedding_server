from typing import List

from pydantic import BaseModel, Field

from common.models import LifeCycle


class AppUpdateRequest(BaseModel):
    description: str | None = Field(None, description="앱 설명")
    keywords: List[str] = Field(default=[], description="앱 키워드")


class AppCreateRequest(AppUpdateRequest):
    app_name: str = Field(..., description="APP Name")


class AppResponse(LifeCycle, AppCreateRequest):
    id: str = Field(..., description="앱 ID")
