import asyncio

import pytest
from fastapi import Response

from app.cmd.api.auth_router import create_auth_router
from app.presentation.schema.requests.user_request import (
    CreateUserRequest,
    LoginRequest,
)
from app.presentation.schema.responses.user_response import (
    CreateUserResponse,
    LoginResponse,
)


class StubAuthController:
    async def create(self, request: CreateUserRequest) -> CreateUserResponse:
        return CreateUserResponse(
            name=request.name,
            email=request.email,
            access_token="register-token",
        )

    async def login(self, request: LoginRequest) -> LoginResponse:
        return LoginResponse(
            name="name",
            email=request.email,
            access_token="login-token",
        )


class StubContainer:
    auth_controller = StubAuthController()


def _endpoint(path: str):
    router = create_auth_router(StubContainer())
    return next(route.endpoint for route in router.routes if route.path == path)


@pytest.mark.parametrize(
    ("path", "request_data", "expected_token"),
    [
        (
            "/users/register",
            CreateUserRequest(
                name="name", email="user@example.com", password="password"
            ),
            "register-token",
        ),
        (
            "/login",
            LoginRequest(email="user@example.com", password="password"),
            "login-token",
        ),
    ],
)
def test_auth_endpoint_returns_token_only_in_local_cookie(
    path, request_data, expected_token
):
    """登録・ログイン時のトークンが本文に含まれずローカル用Cookieだけに設定されることを確認する。"""
    response = Response()

    result = asyncio.run(_endpoint(path)(request_data, response))

    assert "access_token" not in result.model_dump()
    cookie = response.headers["set-cookie"]
    assert f"access_token={expected_token}" in cookie
    assert "HttpOnly" in cookie
    assert "SameSite=lax" in cookie
    assert "Secure" not in cookie
    assert "Path=/" in cookie
