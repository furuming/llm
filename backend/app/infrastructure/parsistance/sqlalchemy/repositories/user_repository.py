from sqlalchemy.orm import Session, sessionmaker

from app.domain.contracts.repository.user_contract import UserRepository
from app.domain.entities.user import User
from app.infrastructure.logger.logger import logger
from app.infrastructure.parsistance.sqlalchemy.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: sessionmaker[Session]):
        self.session_factory = session

    def find_by_email(self, email: str) -> User | None:
        logger.info("Finding user by email email=%s", email)
        try:
            with self.session_factory() as session:
                model = session.query(UserModel).filter(UserModel.email == email).first()
        except Exception:
            logger.exception("Failed to find user by email email=%s", email)
            raise

        if model is None:
            logger.info("User not found by email email=%s", email)
            return None

        logger.info("Found user by email user_id=%s", model.id)
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
        )

    def find_by_id(self, user_id: str) -> User | None:
        logger.info("Finding user by id user_id=%s", user_id)
        try:
            with self.session_factory() as session:
                model = session.query(UserModel).filter(UserModel.id == user_id).first()
        except Exception:
            logger.exception("Failed to find user by id user_id=%s", user_id)
            raise

        if model is None:
            logger.info("User not found by id user_id=%s", user_id)
            return None
        logger.info("Found user by id user_id=%s", user_id)
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
        )

    def save(self, user: User) -> User:
        logger.info("Saving user email=%s", user.email)
        try:
            with self.session_factory() as session:
                model = UserModel(
                    name=user.name,
                    email=user.email,
                    password=user.password,
                )

                session.add(model)
                session.commit()
                session.refresh(model)
        except Exception:
            logger.exception("Failed to save user email=%s", user.email)
            raise

        logger.info("Saved user user_id=%s", model.id)
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
        )
