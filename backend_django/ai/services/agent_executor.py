"""Validated application-facing execution boundary for the central AI gateway."""
from typing import Any

from ..exceptions import AIError


class AgentExecutor:
    def __init__(self, user: Any = None):
        self.user = user

    def execute(
        self,
        *,
        provider: str | None,
        messages: list[dict],
        model: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> dict:
        if not isinstance(messages, list) or not messages:
            raise ValueError("At least one message is required.")
        for item in messages:
            if (
                not isinstance(item, dict)
                or item.get("role") not in {"system", "user", "assistant"}
                or not isinstance(item.get("content"), str)
                or not item["content"].strip()
            ):
                raise ValueError("Invalid message format.")

        from .core import AIFallbackChainService

        try:
            return AIFallbackChainService.generate_completion(
                messages=messages,
                user=self.user,
                preferred_provider=provider,
                model=model or None,
                temperature=temperature,
                max_tokens=max_tokens,
                task_type="agent",
            )
        except AIError:
            raise
