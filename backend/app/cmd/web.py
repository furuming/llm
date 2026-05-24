from app.cmd.api.router import create_router
from app.cmd.di.container import Container



container = Container()
app = create_router(container)

def main():
    """webサーバーを起動する"""
    print("start app")




    print("start app")

if __name__ == "__main__":
    main()