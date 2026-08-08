from app.application.usecases.chat_usecase import ChatUsecase
from app.domain.entities.chat_message import ChatMessageEntity


class ChatController:
    def __init__(self, chat_usecase: ChatUsecase):
        """初期化"""
        self.chat_usecase = chat_usecase

    def post_chat(
        self, user_id: str, session_id: str, content: str
    ) -> ChatMessageEntity:
        """チャット送信"""
        return self.chat_usecase.send_message(user_id, session_id, content)
