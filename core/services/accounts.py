from fastapi import HTTPException

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
