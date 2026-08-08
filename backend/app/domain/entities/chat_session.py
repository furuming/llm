from dataclasses import dataclass
from datetime import datetime

from app.domain.entities.chat_message import ChatMessageEntity


@dataclass
class ChatSessionEntity:
    id: str
    title: str | None
    messages: list[ChatMessageEntity]
    created_at: datetime
    updated_at: datetime
