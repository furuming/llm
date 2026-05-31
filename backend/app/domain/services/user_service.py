from app.domain.contracts.repository.user_contract import UserRepository
from app.domain.contracts.security.hasher import Hasher
from app.domain.exception import (UserAlreadyExistsError)
from app.domain.entities.user import User

class UserService:
    def __init__(self, hasher: Hasher, user_repository:UserRepository ):
        self.hasher = hasher
        self.user_repository = user_repository

    def register(self, name, email, password)->User:

        user = self.user_repository.find_by_email(email)
        if user is not None:
            raise UserAlreadyExistsError

        hashed_password = self.hasher.hash(password)

        user = self.user_repository.save(
            User(id=None, name=name, email=email, password=hashed_password)
        )
        return user

        
