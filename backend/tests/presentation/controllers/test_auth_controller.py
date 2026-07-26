import asyncio

from app.domain.entities.user import User
from app.presentation.controllers.auth_controller import AuthController


class StubUserUsecase:
    def get_user_by_id(self, user_id: str) -> User:
        return User(
            id=user_id,
            name="name",
            email="user@example.com",
            password="$2b$12$password-hash",
        )


def test_get_authenticated_user_maps_domain_user_to_safe_response():
    """認証済みユーザーをパスワードを含まないレスポンスへ変換することを確認する。"""
    controller = AuthController(StubUserUsecase())

    response = asyncio.run(controller.get_authenticated_user("01X"))

    assert response.model_dump() == {
        "id": "01X",
        "name": "name",
        "email": "user@example.com",
    }
    assert "password" not in response.model_dump()
