from fastapi import FastAPI, APIRouter, Response
from typing import Callable

from app.cmd.di.container import Container

def create_router( container:Container )->FastAPI:
    
    app = FastAPI()

    set_api_route( router=app, path="/auth", endpoint=container.auth_controller.test, methods=["GET"])
    set_api_route( router=app, path="/users/register", endpoint=container.auth_controller.create, methods=["POST"], response_hook=set_auth_cookie)
    
    return app


def set_api_route(
    router: APIRouter,
    path: str,
    endpoint: Callable,
    methods: list[str],
    response_hook: Callable | None = None,
):
    async def wrapper(
        response: Response,
        *args,
        **kwargs,
    ):
        result = await endpoint(*args, **kwargs)

        if response_hook:
            response_hook(
                response=response,
                result=result,
            )

        return result

    router.add_api_route(
        path,
        wrapper,
        methods=methods,
    )

def set_auth_cookie( response: Response, result)-> None:

    response.set_cookie(
        key="access_token",
        value=result.access_token,
        httponly=True,
        secure=True,
        samesite="lax",
        max_age=3600,
    )
