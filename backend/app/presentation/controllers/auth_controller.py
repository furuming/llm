from app.application.usecases.user_usecase import UserUsecase
from app.infrastructure.logger.logger import logger
from app.presentation.schema.requests.user_request import (
    CreateUserRequest,
    LoginRequest,
)
from app.presentation.schema.responses.user_response import (
    AuthenticatedUserResponse,
    CreateUserResponse,
    LoginResponse,
)


class AuthController:
    def __init__(self, user_usecase: UserUsecase):
        self.user_usecase = user_usecase

    async def get_authenticated_user(
        self, user_id: str
    ) -> AuthenticatedUserResponse:
        logger.info("Get authenticated user request received user_id=%s", user_id)
        try:
            user = self.user_usecase.get_user_by_id(user_id)
        except Exception:
            logger.exception(
                "Get authenticated user request failed user_id=%s", user_id
            )
            raise
        logger.info("Get authenticated user request completed user_id=%s", user_id)
        if user.id is None:
            logger.error("Get authenticated user failed: user id is missing")
            raise ValueError("user id is missing")
        return AuthenticatedUserResponse(
            id=user.id,
            name=user.name,
            email=user.email,
        )

    async def create(self, request: CreateUserRequest) -> CreateUserResponse:
        logger.info("Register request received email=%s", request.email)
        try:
            user = self.user_usecase.register_user(
                name=request.name,
                email=request.email,
                password=request.password,
            )
        except Exception:
            logger.exception("Register request failed email=%s", request.email)
            raise

        logger.info("Register request completed user_id=%s", user.id)
        return CreateUserResponse(
            name=user.name,
            email=user.email,
            access_token=user.jwt,
        )

    async def login(self, request: LoginRequest) -> LoginResponse:
        logger.info("Login request received email=%s", request.email)
        try:
            result = self.user_usecase.login(
                email=request.email, password=request.password
            )
        except Exception:
            logger.exception("Login request failed email=%s", request.email)
            raise

        logger.info("Login request completed user_id=%s", result.id)
        return LoginResponse(
            name=result.name, email=result.email, access_token=result.jwt
        )
