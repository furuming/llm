from abc import ABC, abstractmethod

from app.domain.entities.chat_session import ChatSessionEntity


class ChatSessionContract(ABC):
    """チャットセッションコントラクト"""

    @abstractmethod
    def create(self, entity: ChatSessionEntity) -> ChatSessionEntity:
        """sessionの作成"""
        ...

    @abstractmethod
    def get(self, session_id: str) -> ChatSessionEntity:
        """sessionの取得"""
        ...

    @abstractmethod
    def get_all(self, user_id: str) -> list[ChatSessionEntity]:
        """sessionの一覧取得"""
        ...
