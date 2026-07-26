import logging

from fastapi import APIRouter, Depends, Request, Response

from app.cmd.api.middlewares.auth_middleware import AuthMiddleware
from app.cmd.di.container import Container

logger = logging.getLogger("uvicorn.error")


def create_user_router(container: Container) -> APIRouter:
    router = APIRouter(dependencies=[Depends(AuthMiddleware(container.auth_service))])

    ACCESS_TOKEN = "access_token"

    @router.get("/auth/get_user")
    async def get_user(request: Request, response: Response):

        user_id = request.state.user_id
        result = await container.auth_controller.get_authenticated_user(user_id)

        return result

    return router
