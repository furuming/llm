from datetime import UTC, datetime, timedelta

from app.domain.contracts.security.tokener_contract import TokenerContract


class AuthService:
    def __init__(self, tokener: TokenerContract):
        """初期化"""
        self.tokener = tokener

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
        user_id = decoded.get("user_id")
        if not user_id:
            raise ValueError("jwt payload is missing user_id")
        return user_id
