import datetime
from typing import List, Union

from redis_om import Migrator
from fastapi import APIRouter, Depends, HTTPException

from core.models.accounts import User, format_
from core.schemas.accounts import UserCreateUpdateSchema, UserDetailSchema


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)

Migrator().run()


@router.post("/user")
def create_user(data: UserCreateUpdateSchema):
    exists = User.find(User.username == data.username).first()
    if exists:
        raise HTTPException(status_code=404, detail="Username already exists")

    user = User(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        ranking=data.ranking,
        post_count=0,
        timestamp=datetime.date.today()
    )
    return user.save()


# @router.get("/users", response_model=List[UserDetailSchema])
@router.get("/users")
def fetch_users(user_pk: Union[str, None] = None):
    return User.all_pks()
    if user_pk:
        return [format_(pk) for pk in User.all_pks() if user_pk == pk]
    return [format_(pk) for pk in User.all_pks()]

@router.patch("/user/{pk}", status_code=204)
def delete_user(pk: str):
    return User.delete(pk)
