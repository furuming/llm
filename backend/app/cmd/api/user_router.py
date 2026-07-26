from fastapi import APIRouter, Depends, Request

from app.cmd.api.middlewares.auth_middleware import AuthMiddleware
from app.cmd.di.container import Container
from app.presentation.schema.responses.user_response import (
    AuthenticatedUserResponse,
)


def create_user_router(container: Container) -> APIRouter:
    auth_middleware = AuthMiddleware(container.auth_service)
    router = APIRouter(dependencies=[Depends(auth_middleware)])

    @router.get("/auth/get-user", response_model=AuthenticatedUserResponse)
    async def get_user(request: Request) -> AuthenticatedUserResponse:
        user_id = request.state.user_id
        return await container.auth_controller.get_authenticated_user(user_id)

    return router
