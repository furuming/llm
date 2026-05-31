from app.domain.services.user_service import UserService
from app.domain.entities.user import User
from app.domain.exception import (UserAlreadyExistsError)
from app.application.dto.output.user_output import UserOutput
class UserUsecase:

    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register_user(self, name:str, email:str, password:str)->UserOutput:
        
        user:User = self.user_service.register( name, email,password )

        # TODO: jwt発行
        jwt = "todo"

        
        return UserOutput(
            id = user.id,
            email = user.email,
            name = user.name,
            jwt = jwt
        )
