from fastapi import APIRouter, Request

from app.cmd.di.container import Container


def create_chat_router(container: Container):

    router = APIRouter()

    @router.post("/{session_id}/chats")
    def chat(request: Request, session_id: str, content: str):
        user_id = request.state.user_id
        return container.chat_controller.post_chat(user_id, session_id, content)
