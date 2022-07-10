import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, File, UploadFile

from core.models.accounts import User
from core.models.posts import Post, PostImage, format_post_
from core.schemas.posts import (
    PostCreateUpdateSchema,
    PostDisLikeSchema,
    PostImageListSchema,
    PostImageSchema,
    PostLikeSchema,
    PostListSchema,
)
from core.services.posts import (
    get_post_images_,
    update_post_,
    update_post_dislike_,
    update_post_image_,
    update_post_likes_,
)
from redis_om import Migrator

from core.services.posts import create_post_


router = APIRouter(
    prefix="/articles",
    tags=["articles"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.get("", response_model=List[PostListSchema])
def fetch_posts(post_pk: Optional[str] = None):
    if post_pk:
        return [format_post_(pk) for pk in Post.all_pks() if post_pk == pk]
    return [format_post_(pk) for pk in Post.all_pks()]


@router.post("/create", response_model=List[PostListSchema])
def create_post(data: PostCreateUpdateSchema):
    # TODO Authenticated User
    user = User.get(pk="01G79WRVZFX5TYSAAB5KWN7CJ9")
    post_data = create_post_(user, data)
    return post_data


@router.put("/{pk}/update", response_model=List[PostListSchema])
def update_post(pk: str, data: PostCreateUpdateSchema):
    post_data = update_post_(pk, data)
    return post_data


@router.patch("/{pk}/like", response_model=List[PostListSchema])
def update_post_likes(pk: str, data: PostLikeSchema):
    post_data = update_post_likes_(pk, data)
    return post_data


@router.patch("/{pk}/dislike", response_model=List[PostListSchema])
def update_post_dislikes(pk: str, data: PostDisLikeSchema):
    post_data = update_post_dislike_(pk, data)
    return post_data


@router.get("/{pk}/images", response_model=List[PostImageSchema])
def get_post_images(pk: str):
    post_images = get_post_images_(pk)
    return post_images


@router.patch("/{pk}/upload_image", response_model=PostImageListSchema)
def add_post_image(pk: str, data: UploadFile = File(...)):
    update_post_image_(pk, data)
    return


# TODO Use this endpoint to fetch all ids when there's an issue
@router.patch("/{pk}/delete", status_code=204)
def delete_post(pk: str):
    Post.delete(pk)
    return
