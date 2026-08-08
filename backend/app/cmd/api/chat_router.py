from fastapi import APIRouter, Depends, Request

from app.cmd.api.middlewares.auth_middleware import AuthMiddleware
from app.cmd.di.container import Container
from app.presentation.schema.requests.chat_session_request import (
    CreateChatSessionRequest,
)
from app.presentation.schema.responses.chat_message_response import (
    ChatMessageResponse,
)
from app.presentation.schema.responses.chat_session_response import (
    ChatSessionResponse,
)


def create_chat_router(container: Container):

    auth_middleware = AuthMiddleware(container.auth_service)
    router = APIRouter(dependencies=[Depends(auth_middleware)])

    @router.post("/sessions", response_model=ChatSessionResponse)
    def create_chat_session(
        request: Request, payload: CreateChatSessionRequest
    ) -> ChatSessionResponse:
        user_id = request.state.user_id
        return container.chat_controller.create_chat_session(user_id, payload.title)

    @router.get("/sessions", response_model=list[ChatSessionResponse])
    def list_chat_sessions(request: Request) -> list[ChatSessionResponse]:
        user_id = request.state.user_id
        return container.chat_controller.list_chat_sessions(user_id)

    @router.get(
        "/sessions/{session_id}/chats",
        response_model=list[ChatMessageResponse],
    )
    def list_chat_messages(
        request: Request, session_id: str
    ) -> list[ChatMessageResponse]:
        user_id = request.state.user_id
        return container.chat_controller.list_chat_messages(user_id, session_id)

    @router.post("/sessions/{session_id}/chats")
    def chat(request: Request, session_id: str, content: str):
        user_id = request.state.user_id
        return container.chat_controller.post_chat(user_id, session_id, content)

    return router
