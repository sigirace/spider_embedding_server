from typing import List
from bson import ObjectId
from pydantic import BaseModel, Field
from common.models import LifeCycle


class AppUpdate(BaseModel):
    description: str | None = Field(default=None, description="앱 설명")
    keywords: List[str] = Field(default=[], description="앱 키워드")


class AppDetail(AppUpdate):
    app_name: str = Field(..., description="앱 이름")


class App(AppDetail, LifeCycle):
    id: ObjectId = Field(default_factory=ObjectId, alias="_id")

    class Config:
        arbitrary_types_allowed = True
        populate_by_name = True
