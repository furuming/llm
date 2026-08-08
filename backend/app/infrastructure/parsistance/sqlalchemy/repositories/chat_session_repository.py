from sqlalchemy.orm import Session, sessionmaker

from app.domain.contracts.repository.chat_session_contract import ChatSessionContract
from app.domain.entities.chat_session import ChatSessionEntity
from app.infrastructure.logger import logger
from app.infrastructure.parsistance.sqlalchemy.models.chat_session_model import (
    ChatSessionModel,
)


class SqlAlchemyChatSessionRepository(ChatSessionContract):
    def __init__(self, session: sessionmaker[Session]):
        self.session_maker = session

    def create(self, entity: ChatSessionEntity):
        """sessionの作成"""
        logger.info("Creating chat session")
        try:
            with self.session_maker() as session:
                model = ChatSessionModel()
                session.add(model)
                session.commit()
                session.refresh(model)
                return model.to_entity()
        except Exception:
            logger.exception("Failed to create chat session")
            raise

    def get(self, session_id: str) -> ChatSessionEntity:
        """"""
        logger.info("Getting chat session by session id")
        try:
            with self.session_maker() as session:
                model = (
                    session.query(ChatSessionModel)
                    .filter_by(session_id=session_id)
                    .first()
                )
                if model is None:
                    raise ValueError(f"Chat session not found: {session_id}")
                return model.to_entity()
        except Exception:
            logger.exception("Failed to get chat session")
            raise

    def get_all(self, user_id: str) -> list[ChatSessionEntity]:
        """sessionの一覧取得"""
        with self.session_maker() as session:
            models = session.query(ChatSessionModel).filter_by(user_id=user_id).all()
            return [model.to_entity() for model in models]
