import logging
from fastapi import APIRouter, Request, Response, HTTPException

from app.presentation.controllers.auth_controller import AuthController

logger = logging.getLogger("uvicorn.error")
from app.presentation.schema.requests.user_request import CreateUserRequest, LoginRequest
from app.presentation.schema.responses.user_response import CreateUserResponse, LoginResponse


def create_user_router(auth_controller: AuthController) -> APIRouter:
    router = APIRouter()

    ACCESS_TOKEN = "access_token"

    @router.get("/auth/get_user")
    async def get_user( request:Request, response:Response ) -> str:

        # cookie取得( TODO:ミドルウェア構築 )
        token = request.cookies.get(ACCESS_TOKEN)
        print(token)
        if token is None:
            raise HTTPException(status_code=401, detail="unauthenticated")

        result = await auth_controller.get_user_by_token(token)

        return result

    @router.post("/users/register", response_model=CreateUserResponse)
    async def register_user(
        request: CreateUserRequest,
        response: Response,
    ) -> CreateUserResponse:
        
        try:
            result = await auth_controller.create(request)
        except Exception as e:
            logger.error(
                "Register error: %s - %s",
                type(e).__name__,
                str(e),
                exc_info=True,
            )
            raise HTTPException(status_code=400, detail=f"Registration failed: {str(e)}")
        

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
    async def login( request: LoginRequest, response: Response )->LoginResponse:
        try:
            result = await auth_controller.login(request)

        except Exception as e:
            logger.error(
                "Login error: %s - %s",
                type(e).__name__,
                str(e),
                exc_info=True,
            )
            raise HTTPException(status_code=400, detail=f"Login failed: {str(e)}")
                    
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
