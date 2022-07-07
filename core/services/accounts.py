import os
import shutil
from typing import List
from fastapi import File, HTTPException, UploadFile

from core.models.accounts import User, format_
from core.schemas.accounts import UserCreateUpdateSchema, UserDetailSchema


def update_user_(pk: str, data: UserCreateUpdateSchema):
    try:
        user = User.find(User.pk == pk).first()
    except:
        raise HTTPException(status_code=404, detail="Not found.")

    user.update(first_name=data.first_name, last_name=data.last_name)
    user.save()
    return [format_(pk) for pk in User.all_pks() if user.pk == pk]


def update_user_image_(pk: str, data: UploadFile = File(...)):
    user = User.find(User.pk == pk).first()
    path = f"static/{user.pk}"

    if not os.path.exists(path):
        os.makedirs(path)

    with open(f"{path}/{data.filename}", "wb+") as file_object:
        shutil.copyfileobj(data.file, file_object)

    return [format_(pk) for pk in User.all_pks() if user.pk == pk]
