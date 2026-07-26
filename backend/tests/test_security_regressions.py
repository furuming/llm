import asyncio
import json

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError
import pytest

from app.cmd.api.error_handlers import register_error_handlers
from app.presentation.schema.responses.user_response import (
    AuthenticatedUserResponse,
    LoginResponse,
)
from app.shared.config import Settings


def test_authenticated_user_response_has_no_password_field():
    response = AuthenticatedUserResponse(
        id="01X", name="name", email="user@example.com"
    )

    assert response.model_dump() == {
        "id": "01X",
        "name": "name",
        "email": "user@example.com",
    }
    assert "password" not in AuthenticatedUserResponse.model_fields


def test_validation_error_does_not_reflect_request_body():
    app = FastAPI()
    register_error_handlers(app)

    handler = app.exception_handlers[RequestValidationError]
    request = Request(
        {
            "type": "http",
            "method": "POST",
            "path": "/login",
            "headers": [],
        }
    )
    error = RequestValidationError(
        [{"type": "value_error", "loc": ("body", "email"), "msg": "invalid"}]
    )

    response = asyncio.run(handler(request, error))
    response_text = response.body.decode()

    assert response.status_code == 422
    assert "body" not in json.loads(response_text)
    assert "plain-secret" not in response_text


def test_short_app_key_is_rejected():
    with pytest.raises(ValidationError, match="APP_KEY must be at least 32 characters"):
        Settings(APP_KEY="short")


def test_access_token_is_excluded_from_response_body():
    response = LoginResponse(
        name="name", email="user@example.com", access_token="secret-jwt"
    )

    assert response.access_token == "secret-jwt"
    assert response.model_dump() == {
        "name": "name",
        "email": "user@example.com",
    }
