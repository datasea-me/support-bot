from datetime import datetime

from pydantic import BaseModel


class MessageBaseScheme(BaseModel):
    telegram_user_id: int
    text: str | None
    attachments: bool | None
    answer_to_user: int | None


class MessageCreateScheme(MessageBaseScheme):
    pass


class MessageFromDBScheme(MessageBaseScheme):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
