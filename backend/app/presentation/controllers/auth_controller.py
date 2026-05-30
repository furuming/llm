from app.presentation.schema.requests.user_request import CreateUserRequest
from app.presentation.schema.responses.user_response import CreateUserResponse


class AuthController:
    def __init__(self):
        pass

    async def test(self)->str:
        print("test")
        return "test"
    
    async def create(self, request: CreateUserRequest) -> CreateUserResponse:
        print(f"register name={request.name}, email={request.email}, password={request.password}")

        return CreateUserResponse(
            name=request.name,
            email=request.email,
        )
    
