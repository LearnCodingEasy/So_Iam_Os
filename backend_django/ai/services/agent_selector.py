"""Permission-aware, deterministic AI agent/provider selection helpers."""
from dataclasses import dataclass
from typing import Any
from django.conf import settings
from ..models import AISettings

@dataclass(frozen=True)
class AgentSelection:
    provider: str
    model: str
    reason: str

class AgentSelector:
    """Selects only providers supported by the existing provider factory."""
    @staticmethod
    def select(*, user: Any, message: str = "", provider: str | None = None,
               model: str | None = None, task_type: str = "chat") -> AgentSelection:
        allowed = {"ollama", "openai", "openrouter", "gemini", "deepseek"}
        configured = getattr(settings, "AI_DEFAULT_PROVIDER", "ollama")
        if user is not None and getattr(user, "is_authenticated", False):
            prefs = AISettings.objects.filter(user=user).first()
            if prefs:
                configured = prefs.preferred_provider or configured
                model = model or prefs.preferred_model
        selected = (provider or configured).strip().lower()
        if selected not in allowed:
            raise ValueError(f"Unsupported AI provider: {selected}")
        return AgentSelection(selected, (model or "").strip(), f"provider preference for {task_type}")
