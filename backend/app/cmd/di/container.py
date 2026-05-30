from app.presentation.controllers.auth_controller import AuthController

class Container:
    def __init__(self):
        self.auth_controller = AuthController()

    def get_controller_auth(self)->AuthController:
        return self.auth_controller
    
    