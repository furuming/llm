from app.presentation.schema.requests.user_request import CreateUserRequest
from app.presentation.schema.responses.user_response import CreateUserResponse

from app.application.usecases.user_usecase import UserUsecase


class AuthController:
    def __init__(self, user_usecase:UserUsecase):
        self.user_usecase = user_usecase

    async def test(self)->str:
        print("test")
        return "test"
    
    async def create(self, request: CreateUserRequest) -> CreateUserResponse:
        print(f"register name={request.name}, email={request.email}, password={request.password}")

        # TODO: validation

        self.user_usecase.register_user(name=request.name, email=request.email, password=request.password)

        return CreateUserResponse(
            name=request.name,
            email=request.email,
        )
    
