import datetime
from typing import List, Optional

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
    # image_url: str
    likes: int
    dislikes: int
    rating: int = Rating.Level_1
    timestamp: Optional[datetime.date] = datetime.datetime

    class Config:
        orm_mode = True


class PostImageSchema(BaseModel):
    id: str
    post: str
    image_url: str
    default: bool
    timestamp: Optional[datetime.date] = datetime.datetime

    class Config:
        orm_mode = True


class PostImageListSchema(BaseModel):
    images: List[str]

    class Config:
        orm_mode = True


class PostLikeSchema(BaseModel):
    user: str
    like: bool = False


class PostDisLikeSchema(BaseModel):
    user: str
    dislike: bool = False
