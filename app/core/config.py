
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    TELEGRAM_TOKEN: str
    GROUP_ID: str
    WEBHOOK_DOMAIN: str | None = None
    WEBHOOK_PATH: str | None = None
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
        env_file = '.env'
        env_file_encoding = 'utf-8'


settings = Settings()
