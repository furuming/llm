from app.application.usecases.chat_usecase import ChatUsecase
from app.domain.entities.chat_message import ChatMessageEntity
from app.presentation.schema.responses.chat_message_response import (
    ChatMessageResponse,
)
from app.presentation.schema.responses.chat_session_response import (
    ChatSessionResponse,
)


class ChatController:
    def __init__(self, chat_usecase: ChatUsecase):
        """初期化"""
        self.chat_usecase = chat_usecase

    def create_chat_session(
        self, user_id: str, title: str | None = None
    ) -> ChatSessionResponse:
        session = self.chat_usecase.create_chat_session(user_id, title)
        return ChatSessionResponse(
            id=session.id,
            title=session.title,
            user_id=session.user_id,
            created_at=session.created_at,
            updated_at=session.updated_at,
        )

    def list_chat_sessions(self, user_id: str) -> list[ChatSessionResponse]:
        sessions = self.chat_usecase.get_chat_sessions(user_id)
        return [
            ChatSessionResponse(
                id=session.id,
                title=session.title,
                user_id=session.user_id,
                created_at=session.created_at,
                updated_at=session.updated_at,
            )
            for session in sessions
        ]

    def list_chat_sessions(self, user_id: str) -> list[ChatSessionResponse]:
        sessions = self.chat_usecase.get_chat_sessions(user_id)
        return [
            ChatSessionResponse(
                id=session.id,
                title=session.title,
                user_id=session.user_id,
                created_at=session.created_at,
                updated_at=session.updated_at,
            )
            for session in sessions
        ]

    def list_chat_messages(
        self, user_id: str, session_id: str
    ) -> list[ChatMessageResponse]:
        messages = self.chat_usecase.get_chat_messages(user_id, session_id)
        return [
            ChatMessageResponse(
                id=message.id,
                session_id=message.session_id,
                role=message.role,
                content=message.content,
                created_at=message.created_at,
                updated_at=message.updated_at,
            )
            for message in messages
        ]

    def post_chat(
        self, user_id: str, session_id: str, content: str
    ) -> ChatMessageEntity:
        """チャット送信"""
        return self.chat_usecase.send_message(user_id, session_id, content)
