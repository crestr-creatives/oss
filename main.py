import datetime
from typing import Optional, Union

from fastapi import FastAPI
from redis_om import get_redis_connection
from redis_om import HashModel

from core.routers import accounts, auth, posts

app = FastAPI(title="OSS")

app.include_router(auth.router)
app.include_router(accounts.router)
app.include_router(posts.router)
