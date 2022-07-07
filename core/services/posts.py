import os
import datetime
import shutil

from fastapi import File, HTTPException, UploadFile

from core.models.posts import Post, Rating, format_
from core.schemas.posts import PostCreateUpdateSchema


def create_post_(user: int, data: PostCreateUpdateSchema):
    # TODO Authenticated User
    post = Post(
        author=user.pk,
        title=data.title,
        body=data.body,
        likes=0,
        dislikes=0,
        rating=Rating.Level_0,
        timestamp=datetime.date.today(),
    )
    post.save()
    return [post]


def update_post_(pk: str, data: PostCreateUpdateSchema):
    try:
        post = Post.find(Post.pk == pk).first()
    except:
        raise HTTPException(status_code=404, detail="Not found.")

    post.update(first_name=data.first_name, last_name=data.last_name)
    post.save()
    return [format_(pk) for pk in Post.all_pks() if post.pk == pk]


def update_post_image_(pk: str, data: UploadFile = File(...)):
    post = Post.find(Post.pk == pk).first()
    path = f"static/posts/{post.pk}"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/{data.filename}", "wb+") as file_object:
        shutil.copyfileobj(data.file, file_object)

    return [format_(pk) for pk in Post.all_pks() if post.pk == pk]