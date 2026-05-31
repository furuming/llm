from fastapi import FastAPI

from app.cmd.api.error_handlers import register_error_handlers
from app.cmd.api.user_router import create_user_router
from app.cmd.di.container import Container


def create_router(container: Container) -> FastAPI:
    app = FastAPI(debug=False)
    register_error_handlers(app)
    app.include_router(create_user_router(container.auth_controller))
    return app
