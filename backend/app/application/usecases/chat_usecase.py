from datetime import datetime

from app.domain.entities.chat_message import ChatMessageEntity
from app.domain.entities.chat_session import ChatSessionEntity
from app.domain.services.chat_service import ChatService
from app.domain.services.user_service import UserService
from app.shared.ulid import generate_ulid


class ChatUsecase:
    def __init__(
        self,
        user_service: UserService,
        chat_service: ChatService,
    ):
        """初期化"""
        self.user_service = user_service
        self.chat_service = chat_service

    def create_chat_session(
        self, user_id: str, title: str | None = None
    ) -> ChatSessionEntity:
        """チャットセッション作成"""
        self.user_service.find_by_id(user_id)

        session = ChatSessionEntity(
            id=generate_ulid(),
            title=title,
            user_id=user_id,
            messages=[],
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return self.chat_service.create_chat_session(session)

    def get_chat_sessions(self, user_id: str) -> list[ChatSessionEntity]:
        """チャットセッション一覧取得"""
        self.user_service.find_by_id(user_id)
        return self.chat_service.get_chat_sessions(user_id)

    def get_chat_sessions(self, user_id: str) -> list[ChatSessionEntity]:
        """チャットセッション一覧取得"""
        self.user_service.find_by_id(user_id)
        return self.chat_service.get_chat_sessions(user_id)

    def get_chat_messages(
        self, user_id: str, session_id: str
    ) -> list[ChatMessageEntity]:
        """チャットメッセージ一覧取得"""
        self.user_service.find_by_id(user_id)
        session = self.chat_service.get_chat_session(session_id=session_id)
        return self.chat_service.get_chat_messages(session)

    def send_message(
        self, user_id: str, session_id: str, content: str
    ) -> ChatMessageEntity:
        """メッセージ送信"""
        # user取得
        user = self.user_service.find_by_id(user_id)

        # session取得
        session = self.chat_service.get_chat_session(session_id=session_id)

        ulid = generate_ulid()
        message = ChatMessageEntity(
            id=ulid,
            session_id=session.id,
            role="user",
            content=content,
            created_at=datetime.now(),
            updated_at=datetime.now(),
        )

        return self.chat_service.register_chat_message(message)
