from dataclasses import dataclass
from datetime import datetime


@dataclass
class ChatMessageEntity:
    id: str
    session_id: str
    role: str
    content: str
    created_at: datetime
    updated_at: datetime
