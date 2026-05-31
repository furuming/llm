from app.domain.contracts.repository.user_contract import UserRepository
from app.domain.entities.user import User
from app.infrastructure.parsistance.sqlalchemy.models.user_model import UserModel

from sqlalchemy.orm import Session

class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session
        pass
    
    def find_by_email(self, email: str) -> User | None:
        model = self.session.query(UserModel).filter(UserModel.email == email).first()
        if model is None:
            return None
        
        return User(
            id = model.id,
            name = model.name,
            email = model.email,
            password = model.password
        )

    
    def save(self, user: User) -> User:
        model = UserModel(
            name = user.name,
            email = user.email,
            password = user.password,
        )

        self.session.add(model)
        self.session.flush()
        
        return User(
            id = model.id,
            name = model.name,
            email = model.email,
            password = model.password,
        )

