from pydantic import BaseModel


class CreateChatSessionRequest(BaseModel):
    title: str | None = None
