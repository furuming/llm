import asyncio
import json

from fastapi import FastAPI, Request
from fastapi.exceptions import RequestValidationError

from app.cmd.api.error_handlers import register_error_handlers


def test_validation_error_does_not_reflect_request_body():
    """入力検証エラーの応答にパスワードを含むリクエスト本文が反射されないことを確認する。"""
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
    content = json.loads(response.body)

    assert response.status_code == 422
    assert "body" not in content
    assert "plain-secret" not in response.body.decode()
