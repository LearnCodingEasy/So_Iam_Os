import requests
from django.conf import settings
from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError
from .base import BaseAIProvider, _provider_http_error
from .openai import OpenAIProvider

class DeepSeekProvider(OpenAIProvider):
    """DeepSeek exposes an OpenAI-compatible Chat Completions API."""
    name = "deepseek"

    def __init__(self, user=None):
        BaseAIProvider.__init__(self, user)
        self.api_key = self._user_api_key() or getattr(settings, "DEEPSEEK_API_KEY", "")
        self.base_url = self._validated_base_url(getattr(settings, "DEEPSEEK_BASE_URL", "https://api.deepseek.com"))
        self.default_model = str(self._configured_value("model", getattr(settings, "DEEPSEEK_MODEL", "deepseek-chat"))).strip()
        if not self.api_key:
            raise AIConfigurationError("DeepSeek API key is not configured.")

    def list_models(self):
        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}/models",
                headers=self._headers(), timeout=self._request_timeout(max(2, int(getattr(settings, "AI_MODEL_DISCOVERY_TIMEOUT_SECONDS", 6)))),
            )
        except requests.Timeout as exc:
            raise AIProviderError("DeepSeek request timed out.", category="timeout", retryable=True) from exc
        except requests.ConnectionError as exc:
            raise AIProviderError("DeepSeek connection failed.", category="network_error", retryable=True) from exc
        except requests.RequestException as exc:
            raise AIProviderError("DeepSeek request failed.", category="network_error", retryable=True) from exc
        if not response.ok:
            raise _provider_http_error(self.name, response)
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("DeepSeek returned invalid JSON.") from exc
        return [
            {"id": item.get("id"), "name": item.get("id"), "capabilities": ["chat"]}
            for item in data.get("data", []) if item.get("id")
        ]



