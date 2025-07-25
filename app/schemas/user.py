from datetime import datetime

from pydantic import BaseModel, Field


class UserBaseScheme(BaseModel):
    telegram_id: int
    telegram_username: str | None = Field(None, max_length=100)
    is_banned: bool | None
    first_name: str | None = Field(None, max_length=100)
    last_name: str | None = Field(None, max_length=100)
    is_admin: bool | None = Field(None)


class UserCreateScheme(UserBaseScheme):
    pass


class UserFromDBScheme(UserBaseScheme):
    id: int
    is_banned: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
