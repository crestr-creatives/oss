import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI
from redis_om import get_redis_connection


env_path = Path(".") / ".env"
load_dotenv(dotenv_path=env_path)

app = FastAPI()

redis = get_redis_connection(
    host=os.getenv("HOST"),
    port=os.getenv("PORT"),
    password=os.getenv("PASSWORD"),
    decode_responses=True,
)
