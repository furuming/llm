from app.presentation.schema.responses.user_response import (
    AuthenticatedUserResponse,
    LoginResponse,
)


def test_authenticated_user_response_has_no_password_field():
    """認証済みユーザーのレスポンス定義にパスワード項目が存在しないことを確認する。"""
    response = AuthenticatedUserResponse(
        id="01X", name="name", email="user@example.com"
    )

    assert response.model_dump() == {
        "id": "01X",
        "name": "name",
        "email": "user@example.com",
    }
    assert "password" not in AuthenticatedUserResponse.model_fields


def test_access_token_is_excluded_from_serialized_response():
    """アクセストークンがレスポンスのシリアライズ結果から除外されることを確認する。"""
    response = LoginResponse(
        name="name", email="user@example.com", access_token="secret-jwt"
    )

    assert response.access_token == "secret-jwt"
    assert response.model_dump() == {
        "name": "name",
        "email": "user@example.com",
    }
