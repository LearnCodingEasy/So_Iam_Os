"""Backward-compatible provider exports; implementations live in ai.providers."""

from ..providers.base import BaseAIProvider, _provider_http_error
from ..providers.openai import OpenAIProvider
from ..providers.gemini import GeminiProvider
from ..providers.ollama import OllamaProvider
from ..providers.deepseek import DeepSeekProvider
from ..providers.openrouter import OpenRouterProvider
from ..providers import get_ai_provider, AIProviderFallbackChain

__all__ = [
    "BaseAIProvider",
    "OpenAIProvider",
    "GeminiProvider",
    "OllamaProvider",
    "DeepSeekProvider",
    "OpenRouterProvider",
    "get_ai_provider",
    "AIProviderFallbackChain",
    "_provider_http_error",
]
