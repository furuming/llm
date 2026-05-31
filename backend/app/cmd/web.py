import uvicorn
from app.cmd.api.router import create_router
from app.cmd.di.container import Container
from app.shared.config import Settings

def create_app( settings: Settings ):
    """webサーバーを起動する"""
    container = Container(settings)
    app = create_router(container)
    return app

settings = Settings()
app = create_app(settings)
