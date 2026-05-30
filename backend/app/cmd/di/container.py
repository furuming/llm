from app.presentation.controllers.auth_controller import AuthController
from app.application.usecases.user_usecaase import UserUsecase

class Container:
    def __init__(self):

        uu = UserUsecase()

        self.auth_controller = AuthController(uu)

    def get_controller_auth(self)->AuthController:
        return self.auth_controller
    
    