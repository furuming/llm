from sqlalchemy.orm import Session, sessionmaker

from app.domain.contracts.repository.user_contract import UserRepository
from app.domain.entities.user import User
from app.infrastructure.parsistance.sqlalchemy.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: sessionmaker[Session]):
        self.session_factory = session

    def find_by_email(self, email: str) -> User | None:
        with self.session_factory() as session:
            model = session.query(UserModel).filter(UserModel.email == email).first()

        if model is None:
            return None

        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
        )

    def find_by_id(self, user_id: str) -> User | None:
        with self.session_factory() as session:
            model = session.query(UserModel).filter(UserModel.id == user_id).first()

        if model is None:
            return None
        return User(
            id=model.id,
            name=model.name,
            email=model.email,
            password=model.password,
        )

    def save(self, user: User) -> User:
        with self.session_factory() as session:
            model = UserModel(
                name=user.name,
                email=user.email,
                password=user.password,
            )

            session.add(model)
            session.commit()
            session.refresh(model)

            return User(
                id=model.id,
                name=model.name,
                email=model.email,
                password=model.password,
            )
