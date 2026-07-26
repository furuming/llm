import pytest
from pydantic import ValidationError

from app.shared.config import Settings


def test_short_app_key_is_rejected():
    """32文字未満のJWT署名鍵が設定エラーとして拒否されることを確認する。"""
    with pytest.raises(ValidationError, match="APP_KEY must be at least 32 characters"):
        Settings(APP_KEY="short")


def test_app_key_with_at_least_32_characters_is_accepted():
    """32文字以上のJWT署名鍵が設定値として受理されることを確認する。"""
    settings = Settings(APP_KEY="x" * 32)

    assert settings.APP_KEY == "x" * 32
