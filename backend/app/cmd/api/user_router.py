from fastapi import APIRouter, Response, HTTPException

from app.presentation.controllers.auth_controller import AuthController
from app.presentation.schema.requests.user_request import CreateUserRequest, LoginRequest
from app.presentation.schema.responses.user_response import CreateUserResponse, LoginResponse


def create_user_router(auth_controller: AuthController) -> APIRouter:
    router = APIRouter()

    @router.get("/auth")
    async def test() -> str:
        return await auth_controller.test()

    @router.post("/users/register", response_model=CreateUserResponse)
    async def register_user(
        request: CreateUserRequest,
        response: Response,
    ) -> CreateUserResponse:
        
        try:
            result = await auth_controller.create(request)
        except Exception:
            raise HTTPException(status_code=400, detail="invalid request")
        

        response.set_cookie(
            key="access_token",
            value=result.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600,
        )
        return result
    
    @router.post("/login")
    async def login( request: LoginRequest, response: Response )->LoginResponse:
        try:
            result = await auth_controller.login(request)

        except Exception:
            raise HTTPException(status_code=400, detail="invalid request")
                    
        response.set_cookie(
            key="access_token",
            value=result.access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            max_age=3600,
        )
        return result

    return router
