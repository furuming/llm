from app.presentation.controllers.auth_controller import AuthController
from app.application.usecases.user_usecase import UserUsecase
from app.domain.services.user_service import UserService

from app.infrastructure.parsistance.sqlalchemy.core.session import create_session_factory
from app.infrastructure.parsistance.sqlalchemy.repositories.user_repository import SQLAlchemyUserRepository

from app.shared.config import Settings
from app.infrastructure.gateways.security.bcyipt_hasher import BcryptHasher

class Container:
    def __init__(self, settings: Settings):

        db_session = create_session_factory( settings.db_url )
        hasher = BcryptHasher()

        ur = SQLAlchemyUserRepository(session=db_session)
        us = UserService(hasher=hasher, user_repository=ur)
        uu = UserUsecase(us)

        self.auth_controller = AuthController(uu)

    def get_controller_auth(self)->AuthController:
        return self.auth_controller
    
    