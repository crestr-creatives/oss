from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from redis_om import NotFoundError

from core.models.accounts import User
from core.schemas.auth import (
    LoginSchema,
    RegisterUserSchema,
)
from core.schemas.auth import Token
from core.utils import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)


router = APIRouter(
    prefix="/auth",
    tags=["auth"],
    responses={404: {"description": "Not found"}},
    # dependencies=[Depends(get_current_user)],
)


@router.post("/login")
def login(data: OAuth2PasswordRequestForm = Depends()):
    user = User.find(User.email == data.username).first()
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials.")

    if not verify_password(data.password, user.password):
        raise HTTPException(status_code=400, detail="Incorrect password.")

    access_token = create_access_token(data={"sub": user.email})
    data = {"email": user.email, "access_token": access_token, "token_type": "bearer"}
    return data


@router.post("/register")
def register(data: RegisterUserSchema):
    is_registered = None
    try:
        is_registered = User.find(User.email == data.email).first()
    except NotFoundError:
        pass

    if is_registered:
        raise HTTPException(
            status_code=400,
            detail="A registered account with this email already exists.",
        )

    user = User(
        email=data.email,
        username=data.username,
        password=get_password_hash(data.password),
        first_name=data.first_name,
        last_name=data.last_name,
        post_count=0,
        timestamp=str(datetime.now().date()),
    )
    user.save()
    access_token = create_access_token(data={"sub": user.email})
    data = {"email": user.email, "access_token": access_token, "token_type": "bearer"}
    return data
