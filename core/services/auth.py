from fastapi import HTTPException
from redis_om import NotFoundError

from core.models.accounts import User, format_
from core.utils import get_password_hash, verify_password


def change_password_(pk, data):
    try:
        user = User.find(User.pk == pk).first()
    except NotFoundError:
        raise HTTPException(status_code=404, detail="Not Found")

    if not verify_password(data.old_password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password.")

    user.password = get_password_hash(data.new_password)
    user.save()
    return [format_(user) for user in User.all_pks() if pk == format_(user)["id"]]
