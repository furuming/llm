from datetime import datetime

from sqlalchemy import DateTime, Index, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.domain.entities.chat_session import ChatSessionEntity
from app.infrastructure.parsistance.sqlalchemy.core.base import Base
from app.infrastructure.parsistance.sqlalchemy.models.chat_message_model import (
    ChatMessageModel,
)


class ChatSessionModel(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[str] = mapped_column(String(26), primary_key=True)
    title: Mapped[str | None] = mapped_column(String(255), nullable=True)
    user_id: Mapped[str] = mapped_column(String(26), nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )

    messages: Mapped[list[ChatMessageModel]] = relationship(
        "ChatMessageModel", back_populates="session", cascade="all, delete-orphan"
    )

    __table_args__ = (Index("ix_chat_sessions_created_at", "created_at"),)

    def to_entity(self) -> ChatSessionEntity:
        return ChatSessionEntity(
            id=self.id,
            title=self.title,
            user_id=self.user_id,
            messages=[message.to_entity() for message in self.messages],
            created_at=self.created_at,
            updated_at=self.updated_at,
        )
