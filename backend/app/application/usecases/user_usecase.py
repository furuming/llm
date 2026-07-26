from app.application.dto.output.user_output import UserOutput
from app.domain.entities.user import User
from app.domain.services.user_service import UserService


class UserUsecase:
    def __init__(self, user_service: UserService):
        self.user_service = user_service

    def register_user(self, name: str, email: str, password: str) -> UserOutput:

        user: User = self.user_service.register(name, email, password)

        if user.id is None:
            print("Exception")
            raise Exception

        jwt = self.user_service.issueJWT(user.id)

        return UserOutput(id=user.id, email=user.email, name=user.name, jwt=jwt)

    def get_user_by_id(self, user_id: str) -> User:

        return self.user_service.find_by_id(user_id)

    def login(self, email: str, password: str) -> UserOutput:

        user: User = self.user_service.login(email, password)

        if user.id is None:
            print("Exception")
            raise Exception

        jwt = self.user_service.issueJWT(user.id)

        return UserOutput(id=user.id, email=user.email, name=user.name, jwt=jwt)
