import os
from typing import Optional

from pydantic_settings import BaseSettings
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    GROUP_ID: str
    WEBHOOK_DOMAIN: Optional[str] = None
    WEBHOOK_PATH: Optional[str] = None
    APP_HOST: str
    APP_PORT: int
    DATABASE_URL: str
    DB_HOST: str
    DB_PORT: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    START_MESSAGE: str
    MESSAGE_THREAD_ID: int

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
