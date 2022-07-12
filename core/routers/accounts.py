import datetime
from typing import List, Union

from redis_om import Migrator
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from core.models.accounts import User, format_
from core.schemas.accounts import UserCreateUpdateSchema, UserDetailSchema
from core.services.accounts import update_user_, update_user_image_
from core.utils import get_current_user


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    dependencies=[Depends(get_current_user)],
)


@router.get("/users", response_model=List[UserDetailSchema])
def fetch_users(user_pk: Union[str, None] = None):
    if user_pk:
        return [format_(pk) for pk in User.all_pks() if user_pk == pk]
    return [format_(pk) for pk in User.all_pks()]


@router.put("/user/{pk}/detail", response_model=List[UserDetailSchema])
def update_user(pk: str, data: UserCreateUpdateSchema):
    user_data = update_user_(pk, data)
    return user_data


@router.patch("/user/{pk}/upload_image", response_model=List[UserDetailSchema])
def update_user_image(pk: str, data: UploadFile = File(...)):
    user_data = update_user_image_(pk, data)
    return user_data


@router.patch("/user/{pk}/delete", status_code=204)
def delete_user(pk: str):
    return User.delete(pk)
