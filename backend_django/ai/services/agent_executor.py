"""Thin, validated execution boundary for AI providers."""
from typing import Any
from ..providers import get_ai_provider
from ..exceptions import AIError

class AgentExecutor:
    def __init__(self, user: Any = None):
        self.user = user
    def execute(self, *, provider: str, messages: list[dict], model: str | None = None,
                temperature: float | None = None, max_tokens: int | None = None) -> dict:
        if not isinstance(messages, list) or not messages:
            raise ValueError("At least one message is required.")
        for item in messages:
            if not isinstance(item, dict) or item.get("role") not in {"system", "user", "assistant"} or not isinstance(item.get("content"), str):
                raise ValueError("Invalid message format.")
        try:
            return get_ai_provider(provider, user=self.user).generate(
                messages=messages, model=model or None, temperature=temperature, max_tokens=max_tokens)
        except AIError:
            raise
