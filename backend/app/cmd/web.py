import uvicorn
from app.cmd.api.router import create_router
from app.cmd.di.container import Container
from app.shared.config import Settings

def main():
    """webサーバーを起動する"""
    print("start app")



    settings = Settings()
    print(settings.APP_PORT)

    container = Container()
    app = create_router(container)

    uvicorn.run(app, port=settings.APP_PORT, host="0.0.0.0", log_level="info" )



if __name__ == "__main__":
    main()