import datetime
from typing import List, Optional

from pydantic import BaseModel

from core.models.accounts import Ranking


class UserCreateUpdateSchema(BaseModel):
    first_name: str
    last_name: str

    class Config:
        orm_mode = True


class UserDetailSchema(BaseModel):
    id: str
    first_name: str
    last_name: str
    username: str
    image_url: List[str]
    post_count: Optional[int]
    ranking: str
    timestamp: Optional[datetime.date]

    class Config:
        orm_mode = True
