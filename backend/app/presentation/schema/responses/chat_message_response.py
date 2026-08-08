from datetime import datetime

from pydantic import BaseModel


class ChatMessageResponse(BaseModel):
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime
    updated_at: datetime
