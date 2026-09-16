import requests

from django.conf import settings

from .exceptions import (
    AIConfigurationError,
    AIProviderError,
    AIResponseError,
)


class BaseAIProvider:
    """
    Base interface for all AI providers.
    """

    name = None

    def generate(self, messages, model=None):
        raise NotImplementedError


class OllamaProvider(BaseAIProvider):
    name = "ollama"

    def __init__(self):
        self.base_url = getattr(
            settings,
            "OLLAMA_BASE_URL",
            "http://127.0.0.1:11434",
        )

        self.default_model = getattr(
            settings,
            "OLLAMA_MODEL",
            "llama3.2",
        )

    def generate(self, messages, model=None):
        selected_model = model or self.default_model

        payload = {
            "model": selected_model,
            "messages": messages,
            "stream": False,
        }

        try:
            response = requests.post(
                f"{self.base_url.rstrip('/')}/api/chat",
                json=payload,
                timeout=120,
            )

        except requests.RequestException as exc:
            raise AIProviderError(
                f"Ollama connection failed: {exc}"
            ) from exc

        if not response.ok:
            raise AIProviderError(
                f"Ollama returned HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError(
                "Ollama returned invalid JSON."
            ) from exc

        content = (
            data.get("message", {})
            .get("content", "")
            .strip()
        )

        if not content:
            raise AIResponseError(
                "Ollama returned an empty response."
            )

        return {
            "content": content,
            "provider": self.name,
            "model": selected_model,
            "raw": data,
        }


class OpenRouterProvider(BaseAIProvider):
    name = "openrouter"

    def __init__(self):
        self.api_key = getattr(
            settings,
            "OPENROUTER_API_KEY",
            "",
        )

        self.base_url = getattr(
            settings,
            "OPENROUTER_BASE_URL",
            "https://openrouter.ai/api/v1",
        )

        self.default_model = getattr(
            settings,
            "OPENROUTER_MODEL",
            "openai/gpt-4o-mini",
        )

        if not self.api_key:
            raise AIConfigurationError(
                "OPENROUTER_API_KEY is not configured."
            )

    def generate(self, messages, model=None):
        selected_model = model or self.default_model

        payload = {
            "model": selected_model,
            "messages": messages,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(
                f"{self.base_url.rstrip('/')}/chat/completions",
                json=payload,
                headers=headers,
                timeout=120,
            )

        except requests.RequestException as exc:
            raise AIProviderError(
                f"OpenRouter connection failed: {exc}"
            ) from exc

        if not response.ok:
            raise AIProviderError(
                f"OpenRouter returned HTTP {response.status_code}: "
                f"{response.text[:500]}"
            )

        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError(
                "OpenRouter returned invalid JSON."
            ) from exc

        try:
            content = (
                data["choices"][0]["message"]["content"]
                .strip()
            )
        except (KeyError, IndexError, TypeError) as exc:
            raise AIResponseError(
                "OpenRouter returned an invalid response."
            ) from exc

        if not content:
            raise AIResponseError(
                "OpenRouter returned an empty response."
            )

        return {
            "content": content,
            "provider": self.name,
            "model": selected_model,
            "raw": data,
        }


def get_ai_provider(provider_name):
    """
    Provider factory.
    """

    providers = {
        "ollama": OllamaProvider,
        "openrouter": OpenRouterProvider,
    }

    provider_class = providers.get(provider_name)

    if not provider_class:
        raise AIConfigurationError(
            f"Unsupported AI provider: {provider_name}"
        )

    return provider_class()
