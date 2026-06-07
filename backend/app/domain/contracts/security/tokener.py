from abc import ABC, abstractmethod
from typing import Any

class Tokener(ABC):

    @abstractmethod
    def encode(
        self,
        payload: dict[str, Any],
    ) -> str:
        """payloadからトークン文字列を発行する"""
        raise NotImplementedError


    @abstractmethod
    def decode(
        self,
        token: str,
    ) -> dict[str, Any]:
        """トークン文字列を検証し、payloadを返す"""
        raise NotImplementedError

