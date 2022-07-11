from email.policy import default
import os
import datetime
from enum import Enum
from typing import List, Optional

from redis_om import Field, HashModel

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
    # image_url: str
    likes: int
    dislikes: int
    rating: int = Rating.Level_1
    timestamp: Optional[datetime.date] = datetime.datetime

    class Meta:
        database = DATABASE


class PostImage(HashModel):
    post: str = Field(index=True)
    image_url: str
    default: str
    timestamp: Optional[datetime.date] = datetime.datetime

    class Meta:
        database = DATABASE


class PostLike(HashModel):
    post: str = Field(index=True)
    user: str = Field(index=True)
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

    def get_default_image_url():
        try:
            post_image = PostImage.find(
                (PostImage.post == post) & (PostImage.default == True)
            )
        except:
            post_image = PostImage.find(PostImage.post == post).first()
        return post_image

    return {
        "id": post.pk,
        "author": post.pk,
        "title": post.title,
        "body": post.body,
        # "image_url": get_default_image_url(),
        "likes": post.likes,
        "dislikes": post.dislikes,
        "rating": post.rating,
        "timestamp": post.timestamp,
    }


def format_post_image_(pk: str):
    post_image = PostImage.get(pk)

    return {
        "id": post_image.pk,
        "post": post_image.post,
        "image_url": post_image.image_url,
        "default": post_image.default,
        "timestamp": post_image.timestamp,
    }


def format_likes_(pk: str):
    post_like = PostLike.get(pk)

    return {"id": post_like.pk, "post": post_like.post, "user": post_like.user}


def format_dislikes_(pk: str):
    post_dislike = PostDislike.get(pk)

    return {"id": post_dislike.pk, "post": post_dislike.post, "user": post_dislike.user}
