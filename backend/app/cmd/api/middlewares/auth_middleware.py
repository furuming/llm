from fastapi import HTTPException, Request

from app.domain.services.auth_service import AuthService


class AuthMiddleware:
    """認証を行う"""

    def __init__(self, auth_service: AuthService):
        self.auth_service = auth_service

    def __call__(self, request: Request):
        """jwtを検証する"""
        jwt = request.cookies.get("access_token", None)
        if jwt is None:
            raise HTTPException(status_code=401, detail="authentication error")

        try:
            user_id = self.auth_service.decodeJWT(jwt)
        except (ValueError, KeyError) as exc:
            raise HTTPException(status_code=401, detail="authentication error") from exc

        if not user_id:
            raise HTTPException(status_code=401, detail="authentication error")

        request.state.user_id = user_id
