from datetime import datetime

from sqlalchemy import (
    CheckConstraint,
    DateTime,
    ForeignKey,
    Index,
    String,
    Text,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.chat_message import ChatMessageEntity
from app.infrastructure.parsistance.sqlalchemy.core.base import Base


class ChatMessageModel(Base):
    __tablename__ = "chat_messages"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    session_id: Mapped[str] = mapped_column(
        String(26), ForeignKey("chat_sessions.id"), nullable=False, index=True
    )
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    session: Mapped[ChatSessionModel] = relationship(
        "ChatSessionModel", back_populates="messages"
    )

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

    def update_from_entity(self, message: ChatMessageEntity):
        self.role = message.role
        self.content = message.content
