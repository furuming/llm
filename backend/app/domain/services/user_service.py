from datetime import UTC, datetime, timedelta

from app.domain.contracts.repository.user_contract import UserRepository
from app.domain.contracts.security.hasher_contract import HasherContract
from app.domain.contracts.security.tokener_contract import TokenerContract
from app.domain.entities.user import User
from app.domain.exception import (
    InvalidPasswordError,
    UserAlreadyExistsError,
    UserNotFoundError,
)


class UserService:
    def __init__(
        self,
        hasher: HasherContract,
        tokener: TokenerContract,
        user_repository: UserRepository,
    ):
        """初期化"""
        self.hasher = hasher
        self.tokener = tokener
        self.user_repository = user_repository

    def register(self, name, email, password) -> User:

        user = self.user_repository.find_by_email(email)
        if user is not None:
            print("UserAlreadyExistsError")
            raise UserAlreadyExistsError

        hashed_password = self.hasher.hash(password)

        user = self.user_repository.save(
            User(id=None, name=name, email=email, password=hashed_password)
        )

        return user

    def find_by_id(self, user_id: str) -> User:

        user = self.user_repository.find_by_id(user_id)
        if user is None:
            print("UserNotFoundError")
            raise UserNotFoundError
        return user

    def login(self, email: str, password: str) -> User:

        user = self.user_repository.find_by_email(email)

        if user is None:
            print("UserNotFoundError")
            raise UserNotFoundError

        if user.password is None:
            raise

        if not self.hasher.verify(password, user.password):
            print("InvalidPasswordError")
            raise InvalidPasswordError

        return user

    def issueJWT(self, user_id: str) -> str:
        """jwtを発行する"""
        expired_at: datetime = datetime.now(UTC) + timedelta(hours=2)

        jwt = self.tokener.encode(
            {"user_id": user_id, "exp": int(expired_at.timestamp())}
        )
        return jwt

    def decodeJWT(self, token) -> str:
        """jwtを復号化しuser_idを取得する"""
        decoded = self.tokener.decode(token)
        return decoded.get("user_id", "")
