from abc import ABC, abstractmethod

from app.domain.entities.chat_message import ChatMessageEntity


class ChatMessageContract(ABC):
    @abstractmethod
    def create(self, message: ChatMessageEntity) -> ChatMessageEntity:
        """メッセージ作成"""
        ...

    @abstractmethod
    def get_all(self, chat_session_id: str) -> list[ChatMessageEntity]:
        """全件取得"""
        ...

    @abstractmethod
    def get_by_id(self, chat_session_id: str, message_id: str) -> ChatMessageEntity:
        """1件取得"""
        ...

    @abstractmethod
    def delete(self, chat_session_id: str, message_id: str):
        """削除"""
        ...

    @abstractmethod
    def update(self, message: ChatMessageEntity) -> ChatMessageEntity:
        """更新"""
        ...
