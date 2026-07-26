import bcrypt

from app.domain.contracts.security.hasher_contract import HasherContract
from app.infrastructure.logger.logger import logger


class BcryptHasher(HasherContract):
    def hash(self, text: str) -> str:
        logger.info("Hashing password")
        try:
            hashed = bcrypt.hashpw(text.encode("utf-8"), bcrypt.gensalt()).decode(
                "utf-8"
            )
        except Exception:
            logger.exception("Failed to hash password")
            raise
        logger.info("Password hashed")
        return hashed

    def verify(self, text: str, hashed: str) -> bool:
        logger.info("Verifying password")
        try:
            verified = bcrypt.checkpw(
                text.encode("utf-8"), hashed_password=hashed.encode("utf-8")
            )
        except Exception:
            logger.exception("Failed to verify password")
            raise
        logger.info("Password verification completed")
        return verified
