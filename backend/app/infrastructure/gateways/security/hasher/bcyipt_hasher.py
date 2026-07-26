import bcrypt

from app.domain.contracts.security.hasher_contract import HasherContract


class BcryptHasher(HasherContract):
    def hash(self, text: str) -> str:
        return bcrypt.hashpw(text.encode("utf-8"), bcrypt.gensalt()).decode("utf-8")

    def verify(self, text: str, hashed: str) -> bool:
        return bcrypt.checkpw(
            text.encode("utf-8"), hashed_password=hashed.encode("utf-8")
        )
