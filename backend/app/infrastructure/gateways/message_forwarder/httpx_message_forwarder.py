from datetime import datetime

import httpx

from app.domain.contracts.gateway.message_forwarder_contract import (
    MessageForwarderContract,
)
from app.domain.entities.chat_message import ChatMessageEntity
from app.infrastructure.logger.logger import logger
from app.shared.ulid import generate_ulid


class HttpxMessageForwarder(MessageForwarderContract):
    def __init__(self, llm_server_host: str):
        self.llm_server_host = llm_server_host

    def forward(self, message: ChatMessageEntity) -> ChatMessageEntity | None:
        if not self.llm_server_host:
            return None

        payload = {
            "id": message.id,
            "session_id": message.session_id,
            "role": message.role,
            "content": message.content,
            "created_at": message.created_at.isoformat(),
            "updated_at": message.updated_at.isoformat(),
        }

        try:
            with httpx.Client(timeout=10.0) as client:
                response = client.post(f"{self.llm_server_host}/messages", json=payload)
                response.raise_for_status()
                data = response.json()
        except Exception as exc:
            logger.exception("Failed to forward chat message to LLM server: %s", exc)
            return None

        role = data.get("role", "assistant")
        content = data.get("content")
        if content is None:
            logger.error("LLM response missing content: %s", data)
            return None

        created_at = _parse_datetime(data.get("created_at"))
        updated_at = _parse_datetime(data.get("updated_at"))

        return ChatMessageEntity(
            id=data.get("id", generate_ulid()),
            session_id=data.get("session_id", message.session_id),
            role=role,
            content=content,
            created_at=created_at,
            updated_at=updated_at,
        )


def _parse_datetime(value: str | None) -> datetime:
    if not value:
        return datetime.now()
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        logger.error("Invalid datetime format from LLM response: %s", value)
        return datetime.now()
