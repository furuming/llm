from app.application.usecases.chat_usecase import ChatUsecase
from app.application.usecases.user_usecase import UserUsecase
from app.domain.services.auth_service import AuthService
from app.domain.services.chat_service import ChatService
from app.domain.services.user_service import UserService
from app.infrastructure.gateways.security.hasher.bcyipt_hasher import BcryptHasher
from app.infrastructure.gateways.security.tokener.pyjwt_tokener import PyJwtTokener
from app.infrastructure.parsistance.sqlalchemy.core.session import (
    create_session_factory,
)
from app.infrastructure.parsistance.sqlalchemy.repositories.chat_message_repository import (
    SqlAlchemyChatMessageRepository,
)
from app.infrastructure.parsistance.sqlalchemy.repositories.chat_session_repository import (
    SqlAlchemyChatSessionRepository,
)
from app.infrastructure.parsistance.sqlalchemy.repositories.user_repository import (
    SQLAlchemyUserRepository,
)
from app.presentation.controllers.auth_controller import AuthController
from app.presentation.controllers.chat_controller import ChatController
from app.shared.config import Settings


class Container:
    def __init__(self, settings: Settings):
        db_session = create_session_factory(settings.db_url)
        hasher = BcryptHasher()
        tokener = PyJwtTokener(
            secret_key=settings.APP_KEY,
            algorism=settings.APP_ALGORISM,
        )
        csr = SqlAlchemyChatSessionRepository(db_session)
        cmr = SqlAlchemyChatMessageRepository(db_session)

        ur = SQLAlchemyUserRepository(session=db_session)
        us = UserService(hasher=hasher, tokener=tokener, user_repository=ur)
        cs = ChatService(chat_message=cmr, chat_session=csr)

        self.auth_service = AuthService(tokener=tokener)
        uu = UserUsecase(us)
        cu = ChatUsecase(user_service=us, chat_service=cs)

        self.auth_controller = AuthController(uu)
        self.chat_controller = ChatController(chat_usecase=cu)
