from typing import Any

import jwt

from app.domain.contracts.security.tokener_contract import TokenerContract
from app.infrastructure.logger.logger import logger


class PyJwtTokener(TokenerContract):
    def __init__(self, algorism: str, secret_key: str):
        self.algorism = algorism
        self.secret_key = secret_key

    def encode(self, payload: dict[str, Any]) -> str:
        logger.info("Encoding JWT")
        try:
            token = jwt.encode(payload, self.secret_key, algorithm=self.algorism)
        except Exception:
            logger.exception("Failed to encode JWT")
            raise
        logger.info("JWT encoded")
        return token

    def decode(self, token: str) -> dict[str, Any]:
        logger.info("Decoding JWT")
        try:
            payload = jwt.decode(
                jwt=token, key=self.secret_key, algorithms=self.algorism
            )
        except Exception:
            logger.exception("Failed to decode JWT")
            raise
        logger.info("JWT decoded")
        return payload
