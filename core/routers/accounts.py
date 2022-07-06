import datetime
from typing import List, Union

from redis_om import Migrator
from fastapi import APIRouter, Depends, HTTPException

from core.models.accounts import User, format_
from core.schemas.accounts import UserCreateUpdateSchema, UserDetailSchema
from core.services.accounts import update_user_


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)

Migrator().run()

# TODO Use this endpoint to fetch all ids when there's an issue
# @router.get("/users")
# def fetch_users(user_pk: Union[str, None] = None):
#     return User.all_pks()


@router.get("/users", response_model=List[UserDetailSchema])
def fetch_users(user_pk: Union[str, None] = None):
    if user_pk:
        return [format_(pk) for pk in User.all_pks() if user_pk == pk]
    return [format_(pk) for pk in User.all_pks()]


@router.put("/user/{pk}", response_model=List[UserDetailSchema])
def update_user(pk: str, data: UserCreateUpdateSchema):
    user_data = update_user_(pk, data)
    return user_data


@router.patch("/user/{pk}", status_code=204)
def delete_user(pk: str):
    return User.delete(pk)
