import datetime

from core.models.posts import Post, Rating
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
    return post