import pytest

from app.domain.services.auth_service import AuthService


class DummyTokener:
    def __init__(self, payload=None, error=None):
        self.payload = payload
        self.error = error

    def encode(self, payload):
        return "token"

    def decode(self, token):
        if self.error is not None:
            raise self.error
        return self.payload


def test_decode_jwt_raises_when_user_id_claim_is_missing():
    service = AuthService(DummyTokener(payload={"exp": 123456}))

    with pytest.raises(ValueError, match="user_id"):
        service.decodeJWT("token")


def test_decode_jwt_raises_when_token_is_invalid():
    service = AuthService(DummyTokener(error=ValueError("invalid token")))

    with pytest.raises(ValueError, match="invalid token"):
        service.decodeJWT("token")
