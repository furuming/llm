from app.cmd.api.router import create_router
from app.cmd.di.container import Container
from app.shared.config import Settings


def create_app():
    """webサーバーを起動する"""
    settings = Settings()
    container = Container(settings)
    app = create_router(container)
    return app


app = create_app()
