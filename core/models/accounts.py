import datetime
from enum import Enum, unique
from typing import Any, Optional
from pydantic import EmailStr

from redis_om import Field, HashModel, Migrator

from core.database import redis


class Ranking(str, Enum):
    LEVEL_1 = "Level 1"
    LEVEL_2 = "Level 2"
    LEVEL_3 = "Level 3"
    LEVEL_4 = "Level 4"
    LEVEL_5 = "Level 5"


class User(HashModel):
    first_name: Optional[str]
    last_name: Optional[str]
    email: EmailStr = Field(index=True)
    username: Optional[str] = Field(index=True)
    password: str
    image_url: Optional[str]
    post_count: Optional[int] = None
    ranking: Optional[str] = Ranking.LEVEL_1
    timestamp: datetime.date

    class Meta:
        database = redis


def format_(pk: str):
    user = User.get(pk)

    return {
        "id": user.pk,
        "first_name": user.first_name,
        "last_name": user.last_name,
        "username": user.username,
        "image_url": user.image_url,
        "post_count": user.post_count,
        "ranking": user.ranking,
        "timestamp": user.timestamp,
    }
