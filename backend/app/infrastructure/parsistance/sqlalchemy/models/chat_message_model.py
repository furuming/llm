from sqlalchemy import (
    CheckConstraint,
    Column,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.orm import relationship

from app.domain.entities.chat_message import ChatMessageEntity
from app.infrastructure.parsistance.sqlalchemy.core.base import Base


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id = Column(String(26), primary_key=True)
    session_id = Column(
        String(26), ForeignKey("chat_sessions.id"), nullable=False, index=True
    )
    role = Column(String(20), nullable=False)
    content = Column(Text, nullable=False)
    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    session = relationship("ChatSession", back_populates="messages")

    __table_args__ = (
        Index("ix_chat_messages_session_id_created_at", "session_id", "created_at"),
        CheckConstraint(
            "role IN ('system', 'user', 'assistant', 'tool')",
            name="ck_chat_messages_role",
        ),
    )

    def to_entity(self) -> ChatMessageEntity:
        return ChatMessageEntity(
            id=self.id,
            session_id=self.session_id,
            role=self.role,
            content=self.content,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    def update_from_entity(self, message: MessageEntity):
        self.role = message.role
        self.content = message.content
