from app.domain.contracts.repository.chat_message_contract import ChatMessageContract
from app.domain.contracts.repository.chat_session_contract import ChatSessionContract
from app.domain.entities.chat_message import ChatMessageEntity
from app.domain.entities.chat_session import ChatSessionEntity


class ChatService:
    def __init__(
        self, chat_session: ChatSessionContract, chat_message: ChatMessageContract
    ):
        """初期化"""
        self.chat_session = chat_session
        self.chat_message = chat_message

    def create_chat_session(self, entity: ChatSessionEntity) -> ChatSessionEntity:
        """チャットセッション作成"""
        return self.chat_session.create(entity)

    def get_chat_session(self, session_id: str) -> ChatSessionEntity:
        """チャットセッション取得"""
        return self.chat_session.get(session_id)

    def get_chat_sessions(self, user_id: str) -> list[ChatSessionEntity]:
        """チャットセッション一覧取得"""
        return self.chat_session.get_all(user_id)

    def register_chat_message(self, message: ChatMessageEntity):
        """チャットメッセージ登録"""
        return self.chat_message.create(message)

    def get_chat_messages(
        self, chat_session: ChatSessionEntity
    ) -> list[ChatMessageEntity]:
        """チャットメッセージ一覧取得"""
        return self.chat_message.get_all(chat_session.id)

    def delete_chat_message(self, chat_session: ChatSessionEntity, message_id: str):
        """チャットメッセージ削除"""
        return self.chat_message.delete(chat_session.id, message_id)

    def send_chat(self, user_id: int, chat_session: ChatSessionEntity, content: str):
        """チャット送信"""
