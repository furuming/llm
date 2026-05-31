# domain/contracts/repositories/user_repository.py

from typing import Protocol

from app.domain.entities.user import User


class UserRepository(Protocol):
    def find_by_email(self, email: str) -> User | None:
        ...

    def save(self, user: User) -> User:
        ...
