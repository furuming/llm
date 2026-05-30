import uvicorn
from app.cmd.api.router import create_router
from app.cmd.di.container import Container
from app.shared.config import Settings

def create_app():
    """webサーバーを起動する"""
    container = Container()
    app = create_router(container)
    return app

settings = Settings()
app = create_app()
uvicorn.run(
    "app.cmd.web:app",
    port=settings.APP_PORT,
    host="0.0.0.0",
    log_level="info",
    reload=True
)
