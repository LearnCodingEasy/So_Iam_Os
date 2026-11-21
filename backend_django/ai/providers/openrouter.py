import requests
from django.conf import settings
from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError
from .base import BaseAIProvider, _provider_http_error
from .openai import OpenAIProvider

class OpenRouterProvider(OpenAIProvider):
    name = "openrouter"

    def __init__(self, user=None):
        BaseAIProvider.__init__(self, user)
        self.api_key = self._user_api_key() or getattr(
            settings, "OPENROUTER_API_KEY", "")
        self.base_url = self._validated_base_url(getattr(settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1"))
        self.default_model = str(self._configured_value("model", getattr(settings, "OPENROUTER_MODEL", "openai/gpt-4o-mini"))).strip()
        if not self.api_key:
            raise AIConfigurationError("OpenRouter API key is not configured.")

    def list_models(self):
        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}/models", headers=self._headers(), timeout=self._request_timeout(max(2, int(getattr(settings, "AI_MODEL_DISCOVERY_TIMEOUT_SECONDS", 6)))),
            )
        except requests.Timeout as exc:
            raise AIProviderError("OpenRouter request timed out.", category="timeout", retryable=True) from exc
        except requests.ConnectionError as exc:
            raise AIProviderError("OpenRouter connection failed.", category="network_error", retryable=True) from exc
        except requests.RequestException as exc:
            raise AIProviderError("OpenRouter request failed.", category="network_error", retryable=True) from exc
        if not response.ok:
            raise _provider_http_error(self.name, response)
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("OpenRouter returned invalid JSON.") from exc
        return [{"id": item.get("id"), "name": item.get("name") or item.get("id"), "capabilities": ["chat"]} for item in data.get("data", []) if item.get("id")]




