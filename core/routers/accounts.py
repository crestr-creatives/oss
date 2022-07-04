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


@router.get("/users", response_model=List[UserDetailSchema])
def fetch_users(user_pk: Union[str, None] = None):
    if user_pk:
        return [format_(pk) for pk in User.all_pks() if user_pk == pk]
    return [format_(pk) for pk in User.all_pks()]


@router.post("/user")
def create_user(data: UserCreateUpdateSchema):
    exists = None
    try:
        exists = User.find(User.username == data.username).first()
    except:
        pass

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


@router.put("/user/{pk}", response_model=List[UserCreateUpdateSchema])
def update_user(pk: str, data: UserCreateUpdateSchema):
    try:
        user = User.find(User.pk == pk).first()
    except:
        raise HTTPException(status_code=404, detail="Not found.")

    user.update(
        first_name=data.first_name,
        last_name=data.last_name,
        username=data.username,
        ranking=data.ranking,
    )
    user.save()
    return [user]

@router.patch("/user/{pk}", status_code=204)
def delete_user(pk: str):
    return User.delete(pk)
