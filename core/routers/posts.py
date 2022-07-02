from fastapi import APIRouter, Depends

from core.models.posts import Post, format_, format_


router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)

@router.get("/posts")
def fetch_posts():
    return [format_(pk) for pk in Post.all_pks()]


@router.post("/posts")
def create_post(post: Post):
    return post.save()