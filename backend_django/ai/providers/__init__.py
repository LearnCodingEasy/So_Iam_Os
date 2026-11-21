from .base import BaseAIProvider
from .ollama import OllamaProvider
from .openai import OpenAIProvider
from .gemini import GeminiProvider
from .deepseek import DeepSeekProvider
from .openrouter import OpenRouterProvider

PROVIDERS = {"ollama": OllamaProvider, "openai": OpenAIProvider, "gemini": GeminiProvider, "deepseek": DeepSeekProvider, "openrouter": OpenRouterProvider}

def get_ai_provider(provider_name, user=None):
    from ..exceptions import AIConfigurationError
    cls=PROVIDERS.get(provider_name)
    if not cls: raise AIConfigurationError(f"Unsupported AI provider: {provider_name}")
    return cls(user=user)

class AIProviderFallbackChain:
    """Backward-compatible adapter for legacy cross-module callers."""
    def __init__(self, user=None):
        self.user = user

    def generate(self, *, provider=None, model=None, messages=None, temperature=None, max_tokens=None, **kwargs):
        from ..services.core import AIFallbackChainService
        return AIFallbackChainService.generate_completion(
            messages=messages or [],
            user=self.user,
            preferred_provider=provider,
            model=model,
            temperature=temperature,
            max_tokens=max_tokens,
            **{k: v for k, v in kwargs.items() if k in {"task_type", "conversation", "idempotency_key"}},
        )

__all__ = ["BaseAIProvider", "OllamaProvider", "OpenAIProvider", "GeminiProvider", "DeepSeekProvider", "OpenRouterProvider", "get_ai_provider", "AIProviderFallbackChain"]
