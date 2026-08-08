from abc import ABC, abstractmethod

from app.domain.entities.chat_message import ChatMessageEntity


class MessageForwarderContract(ABC):
    @abstractmethod
    def forward(self, message: ChatMessageEntity) -> ChatMessageEntity | None:
        """Forward a chat message to an external LLM service and return the response message."""
        ...
