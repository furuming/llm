from app.presentation.schema.requests.user_request import CreateUserRequest, LoginRequest
from app.presentation.schema.responses.user_response import CreateUserResponse, LoginResponse

from app.application.usecases.user_usecase import UserUsecase


class AuthController:
    def __init__(self, user_usecase: UserUsecase):
        self.user_usecase = user_usecase

    async def test(self) -> str:
        print("test")
        return "test"
    
    async def create(self, request: CreateUserRequest) -> CreateUserResponse:
        print(f"register name={request.name}, email={request.email}, password={request.password}")

        # TODO: validation

        user = self.user_usecase.register_user(
            name=request.name,
            email=request.email,
            password=request.password,
        )

        return CreateUserResponse(
            name=user.name,
            email=user.email,
            access_token=user.jwt,
        )
    
    async def login( self, request: LoginRequest ) -> LoginResponse:

        # validate

        result = self.user_usecase.login(
            email = request.email,
            password = request.password
        )

        return LoginResponse(
            name = result.name,
            email = result.email,
            access_token = result.jwt            
        )

