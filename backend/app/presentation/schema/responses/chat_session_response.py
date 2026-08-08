from datetime import datetime

from pydantic import BaseModel


class ChatSessionResponse(BaseModel):
    id: str
    title: str | None = None
    user_id: str
    created_at: datetime
    updated_at: datetime
