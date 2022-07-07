import datetime
from enum import Enum
from typing import Optional

from redis_om import HashModel

from core.database import redis


class Rating(str, Enum):
    Level_0 = 0
    Level_1 = 1
    Level_2 = 2
    Level_3 = 3
    Level_4 = 4
    Level_5 = 5


class Post(HashModel):
    author: str
    title: str
    body: str
    likes: int
    dislikes: int
    rating: int = Rating.Level_1
    timestamp: Optional[datetime.date] = datetime.datetime

    class Meta:
        database = redis


def format_(pk: str):
    post = Post.get(pk)

    return {
        "id": post.pk,
        "author": post.pk,
        "title": post.title,
        "body": post.body,
        "likes": post.likes,
        "dislikes": post.dislikes,
        "rating": post.rating,
        "timestamp": post.timestamp,
    }
