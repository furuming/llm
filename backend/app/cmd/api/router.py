from fastapi import FastAPI

from app.cmd.api.auth_router import create_auth_router
from app.cmd.api.chat_router import create_chat_router
from app.cmd.api.error_handlers import register_error_handlers
from app.cmd.api.user_router import create_user_router
from app.cmd.di.container import Container


def create_router(container: Container) -> FastAPI:
    """APIのエンドポイントを構築"""
    app = FastAPI(debug=False)
    register_error_handlers(app)
    app.include_router(create_auth_router(container))
    app.include_router(create_user_router(container))
    app.include_router(create_chat_router(container), prefix="/chat")
    return app
