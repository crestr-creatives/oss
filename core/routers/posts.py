import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends

from core.models.accounts import User
from core.models.posts import Post, Rating, format_
from core.schemas.posts import PostCreateUpdateSchema, PostListSchema
from redis_om import Migrator

from core.services.posts import create_post_


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)

Migrator().run()


@router.get("", response_model=List[PostListSchema])
def fetch_posts(pk: Optional[str] = None):
    if pk:
        return [format_(pk) for pk in Post.all_pks() if pk == pk]
    return [format_(pk) for pk in Post.all_pks()]


@router.post("/create")
def create_post(data: PostCreateUpdateSchema):
    # TODO Authenticated User
    user = User.get(pk="01G79WRVZFX5TYSAAB5KWN7CJ9")
    post_data = create_post_(user, data)
    return post_data


# TODO Use this endpoint to fetch all ids when there's an issue
@router.patch("/{pk}/delete", status_code=204)
def delete_post(pk: str):
    Post.delete(pk)
    return
