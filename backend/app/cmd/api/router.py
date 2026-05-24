from fastapi import FastAPI
from app.cmd.di.container import Container

def create_router( container:Container )->FastAPI:
    
    app = FastAPI()

    app.add_api_route(path="/auth", endpoint=container.auth_controller.test)
    
    
    return app
