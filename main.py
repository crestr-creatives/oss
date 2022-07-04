import datetime
from typing import Optional, Union

from fastapi import FastAPI
from redis_om import get_redis_connection
from redis_om import HashModel

from core.routers import accounts, posts

app = FastAPI()

app.include_router(accounts.router)
app.include_router(posts.router)