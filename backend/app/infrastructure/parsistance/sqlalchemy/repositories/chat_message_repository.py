from sqlalchemy.orm import Session, sessionmaker

from app.domain.contracts.repository.chat_message_contract import ChatMessageContract
from app.domain.entities.chat_message import ChatMessageEntity
from app.domain.exception import ChatMessageNotFoundError
from app.infrastructure.logger.logger import logger
from app.infrastructure.parsistance.sqlalchemy.models.chat_message_model import (
    ChatMessageModel,
)


class SqlAlchemyChatMessageRepository(ChatMessageContract):
    def __init__(self, session_maker: sessionmaker[Session]) -> None:
        self.session_maker = session_maker

    def create(self, message: ChatMessageEntity) -> ChatMessageEntity:

        logger.info("create chat message")

        try:
            with self.session_maker() as session:
                model = ChatMessageModel(
                    id=message.id,
                    session_id=message.session_id,
                    role=message.role,
                    content=message.content,
                )
                session.add(model)
                session.commit()
                session.refresh(model)
        except Exception:
            logger.exception("Failed to create chat message")
            raise

        return model.to_entity()

    def get_all(self, chat_session_id: str) -> list[ChatMessageEntity]:
        """全件取得"""
        try:
            with self.session_maker() as session:
                query = session.query(ChatMessageModel).filter_by(
                    chat_session_id=chat_session_id
                )
                models = query.all()
                entities = [model.to_entity() for model in models]
                return entities

        except Exception:
            logger.exception("Failed to get all chat messages")
            raise

    def get_by_id(self, chat_session_id: str, message_id: str) -> ChatMessageEntity:
        """"""
        with self.session_maker() as session:
            query = session.query(ChatMessageModel).filter_by(
                chat_session_id=chat_session_id,
                id=message_id,
            )
            model = query.first()
            if not model:
                raise ChatMessageNotFoundError(message_id)
            return model.to_entity()

    def delete(self, chat_session_id: str, message_id: str):
        """"""
        with self.session_maker() as session:
            query = session.query(ChatMessageModel).filter_by(
                chat_session_id=chat_session_id,
                id=message_id,
            )
            model = query.first()
            if not model:
                raise ChatMessageNotFoundError(message_id)
            session.delete(model)
            session.commit()

    def update(self, message: ChatMessageEntity) -> ChatMessageEntity:
        """"""
        with self.session_maker() as session:
            query = session.query(ChatMessageModel).filter_by(
                chat_session_id=message.session_id,
                id=message.id,
            )
            model = query.first()
            if not model:
                raise ChatMessageNotFoundError(message.id)
            model.update_from_entity(message)
            session.commit()
            session.refresh(model)  # 更新されたモデルを再取得するため
            return model.to_entity()
