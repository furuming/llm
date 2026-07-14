from app.domain.contracts.repository.user_contract import UserRepository
from app.domain.contracts.security.hasher import Hasher
from app.domain.contracts.security.tokener import Tokener
from app.domain.exception import (UserAlreadyExistsError, UserNotFoundError, InvalidPasswordError)
from app.domain.entities.user import User
from datetime import datetime, timedelta, timezone


class UserService:
    def __init__(self, hasher: Hasher, tokener:Tokener, user_repository:UserRepository ):
        self.hasher = hasher
        self.tokener = tokener
        self.user_repository = user_repository

    def register(self, name, email, password)->User:

        user = self.user_repository.find_by_email(email)
        if user is not None:            
            print("UserAlreadyExistsError")
            raise UserAlreadyExistsError

        hashed_password = self.hasher.hash(password)


        user = self.user_repository.save(
            User(id=None, name=name, email=email, password=hashed_password)
        )


        return user

    def login( self, email: str,  password: str )->User:

        user = self.user_repository.find_by_email(email)

        if user is None:
            print("UserNotFoundError")
            raise UserNotFoundError
        
        if not self.hasher.verify(password, user.password):
            print("InvalidPasswordError")
            raise InvalidPasswordError

        return user

    def issueJWT( self, user_id:str)->str:
        """jwtを発行する"""

        expired_at: datetime = datetime.now(timezone.utc) + timedelta(hours=2)

        jwt = self.tokener.encode({
            "user_id": user_id,
            "exp": int(expired_at.timestamp())
        })
        return jwt

    def decodeJWT( self, token )->str:

        decoded = self.tokener.decode(token)
        return decoded.get("user_id")

        
