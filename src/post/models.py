from datetime import date, datetime
from typing import Optional

from pydantic import BaseModel, Field


class PostResponseV1(BaseModel):
    id: int
    rubrics: Optional[str]
    text: Optional[str]
    created_date: Optional[datetime]
    updated: Optional[datetime]


class PostRequestV1(BaseModel):
    id: Optional[int]
    rubrics: Optional[str]
    text: Optional[str]
    created_date: Optional[datetime]
    updated: Optional[datetime]
    # Field(default_factory=datetime.now)


class PostUpdateRequestV1(BaseModel):
    # id: Optional[int]
    rubrics: Optional[str]
    text: Optional[str]
    # created_date: Optional[datetime]
    # updated: Optional[datetime]


class PostListResponseV1(BaseModel):
    id: int
    text: Optional[str]
