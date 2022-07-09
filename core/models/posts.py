import os
import datetime
from enum import Enum
from typing import List, Optional

from redis_om import HashModel

from core.database import redis

DATABASE = redis


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
    # image_url: Optional[str]
    likes: int
    dislikes: int
    rating: int = Rating.Level_1
    timestamp: Optional[datetime.date] = datetime.datetime

    class Meta:
        database = DATABASE


class PostImages(HashModel):
    post: int
    image_url: str

    class Meta:
        database = DATABASE


class PostLike(HashModel):
    post: str
    user: str
    like: str

    class Meta:
        database = DATABASE


class PostDislike(HashModel):
    post: str
    user: str
    dislike: str

    class Meta:
        database = DATABASE


def format_post_(pk: str):
    post = Post.get(pk)
    IMG_DIR = f"static/posts/{post.pk}/"

    def get_avatar():
        try:
            path = os.listdir(IMG_DIR)
        except FileNotFoundError:
            path = []
        return path

    return {
        "id": post.pk,
        "author": post.pk,
        "title": post.title,
        "body": post.body,
        "image_url": get_avatar(),
        "likes": post.likes,
        "dislikes": post.dislikes,
        "rating": post.rating,
        "timestamp": post.timestamp,
    }


def format_likes_(pk: str):
    post_like = PostLike.get(pk)

    return {"id": post_like.pk, "post": post_like.post, "user": post_like.user}


def format_dislikes_(pk: str):
    post_dislike = PostDislike.get(pk)

    return {"id": post_dislike.pk, "post": post_dislike.post, "user": post_dislike.user}
