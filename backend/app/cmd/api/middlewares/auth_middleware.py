from fastapi import HTTPException, Request

from app.domain.services.auth_service import AuthService
from app.infrastructure.logger.logger import logger


class AuthMiddleware:
    """認証を行う"""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def __call__(self, request: Request):
        """jwtを検証する"""
        token = request.cookies.get("access_token", None)
        if token is None:
            logger.error("Authentication failed: access token is missing")
            raise HTTPException(status_code=401, detail="authentication error")

        try:
            user_id = self.auth_service.decodeJWT(token)
        except (ValueError, KeyError) as exc:
            logger.error(
                "Authentication failed: invalid access token",
                exc_info=(type(exc), exc, exc.__traceback__),
            )
            raise HTTPException(status_code=401, detail="authentication error") from exc

        if not user_id:
            logger.error("Authentication failed: user id is missing")
            raise HTTPException(status_code=401, detail="authentication error")

        logger.info("Authentication completed user_id=%s", user_id)
        request.state.user_id = user_id
