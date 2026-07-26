from fastapi import APIRouter, HTTPException, Response

from app.cmd.di.container import Container
from app.presentation.schema.requests.user_request import (
    CreateUserRequest,
    LoginRequest,
)
from app.presentation.schema.responses.user_response import (
    CreateUserResponse,
    LoginResponse,
)


def create_auth_router(container: Container) -> APIRouter:
    router = APIRouter()

    ACCESS_TOKEN = "access_token"

    @router.post("/users/register", response_model=CreateUserResponse)
    async def register_user(
        request: CreateUserRequest,
        response: Response,
    ) -> CreateUserResponse:
        try:
            result = await container.auth_controller.create(request)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Registration failed: {str(e)}"
            ) from e

        response.set_cookie(
            key=ACCESS_TOKEN,
            value=result.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600,
        )
        return result

    @router.post("/login")
    async def login(request: LoginRequest, response: Response) -> LoginResponse:
        try:
            result = await container.auth_controller.login(request)
        except Exception as e:
            raise HTTPException(
                status_code=400, detail=f"Login failed: {str(e)}"
            ) from e

        response.set_cookie(
            key=ACCESS_TOKEN,
            value=result.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600,
        )
        return result

    return router
