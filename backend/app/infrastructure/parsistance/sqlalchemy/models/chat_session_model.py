from sqlalchemy import (
    Column,
    DateTime,
    Index,
    String,
    func,
)
from sqlalchemy.orm import relationship

from app.domain.entities.chat_session import ChatSessionEntity
from app.infrastructure.parsistance.sqlalchemy.core.base import Base


class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id = Column(String(26), primary_key=True)
    title = Column(String(255), nullable=True)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    messages = relationship(
        "ChatMessage", back_populates="session", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_chat_sessions_created_at", "created_at"),)

    def to_entity(self) -> ChatSessionEntity:
        return ChatSessionEntity(
            id=self.id,
            title=self.title,
            messages=[message.to_entity() for message in self.messages],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
