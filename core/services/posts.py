import os
import datetime
import shutil

from fastapi import File, HTTPException, UploadFile
from core.models.accounts import User

from core.models.posts import (
    Post,
    PostDislike,
    PostDislike,
    PostImage,
    PostLike,
    Rating,
    format_dislikes_,
    format_likes_,
    format_post_,
)
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
    return [format_post_(pk) for pk in Post.all_pks() if post.pk == pk]


def update_post_image_(pk: str, data: UploadFile = File(...)):
    try:
        post = Post.find(Post.pk == pk).first()
    except:
        raise HTTPException(status_code=404, detail="Not found.")

    path = f"static/posts/{post.pk}"
    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/{data.filename}", "wb+") as file_object:
        shutil.copyfileobj(data.file, file_object)

    post_image = PostImage(post=post.pk, image_url=data.filename, default=False)
    post_image.save()

    return [format_post_(pk) for pk in Post.all_pks() if post.pk == pk]


def get_post_images_(pk):
    post_images = [img for img in PostImage.all_pks() if img.post == pk]
    return post_images


def update_post_likes_(pk: str, data: PostLike):
    try:
        post = Post.find(Post.pk == pk).first()
        user = User.find(User.pk == data.user).first()
    except:
        raise HTTPException(status_code=404, detail="Not found.")

    if data.like:
        like = PostLike(post=post.pk, user=user.pk, like=data.like)
        like.save()
        post.likes += 1
        post.save()

    return [format_likes_(pk) for pk in PostLike.all_pks() if post.pk == pk]


def update_post_dislike_(pk: str, data: PostDislike):
    try:
        post = Post.find(Post.pk == pk).first()
        user = User.find(User.pk == data.user).first()
    except:
        raise HTTPException(status_code=404, detail="Not found.")

    if data.dislike:
        dislike = PostDislike(post=post.pk, user=user.pk, dislike=data.dislike)
        dislike.save()
        post.dislikes += 1
        post.save()

    return [format_dislikes_(pk) for pk in PostDislike.all_pks() if post.pk == pk]
