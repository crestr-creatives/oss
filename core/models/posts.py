import datetime
from typing import Optional

from redis_om import HashModel

from core.database import redis


class Post(HashModel):
    title: str
    body: str
    timestamp: Optional[datetime.date] = datetime.datetime

    class Meta:
        database = redis


def format_(pk: str):
    post = Post.get(pk)

    return {
        "id": post.pk,
        "title": post.title,
        "body": post.body,
        "timestamp": post.timestamp,
    }
