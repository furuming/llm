from datetime import datetime

from app.domain.entities.chat_message import ChatMessageEntity
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

    def send_message(
        self, user_id: str, session_id: str, content: str
    ) -> ChatMessageEntity:
        """メッセージ送信"""
        # user取得
        user = self.user_service.find_by_id(user_id)

        # session作成
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
