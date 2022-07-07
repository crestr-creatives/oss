import datetime
from typing import Optional

from pydantic import BaseModel

from core.models.posts import Rating


class PostCreateUpdateSchema(BaseModel):
    title: str
    body: str

    class Config:
        orm_mode = True


class PostListSchema(BaseModel):
    author: str
    title: str
    body: str
    likes: int
    dislikes: int
    rating: int = Rating.Level_1
    timestamp: Optional[datetime.date] = datetime.datetime

    class Config:
        orm_mode = True
