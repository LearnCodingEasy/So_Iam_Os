import requests

from django.conf import settings

from .exceptions import AIConfigurationError, AIProviderError, AIResponseError
from .models import AIProviderCredential


class BaseAIProvider:
    name = None

    def __init__(self, user=None):
        self.user = user

    def generate(self, messages, model=None, temperature=None, max_tokens=None):
        raise NotImplementedError

    def list_models(self):
        raise NotImplementedError

    def _user_api_key(self):
        if not self.user or not self.user.is_authenticated:
            return ""
        credential = AIProviderCredential.objects.filter(
            user=self.user,
            provider=self.name,
        ).first()
        return credential.get_api_key() if credential and credential.has_api_key else ""


class OllamaProvider(BaseAIProvider):
    name = "ollama"

    def __init__(self, user=None):
        super().__init__(user)
        self.base_url = getattr(
            settings, "OLLAMA_BASE_URL", "http://127.0.0.1:11434")
        self.default_model = getattr(settings, "OLLAMA_MODEL", "llama3.2")

    def generate(self, messages, model=None, temperature=None, max_tokens=None):
        selected_model = model or self.default_model
        payload = {"model": selected_model,
                   "messages": messages, "stream": False}
        options = {}
        if temperature is not None:
            options["temperature"] = temperature
        if max_tokens is not None:
            options["num_predict"] = max_tokens
        if options:
            payload["options"] = options
        try:
            response = requests.post(
                f"{self.base_url.rstrip('/')}/api/chat", json=payload, timeout=120)
        except requests.RequestException as exc:
            raise AIProviderError(f"Ollama connection failed: {exc}") from exc
        if not response.ok:
            raise AIProviderError(
                f"Ollama returned HTTP {response.status_code}: {response.text[:500]}")
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("Ollama returned invalid JSON.") from exc
        content = data.get("message", {}).get("content", "").strip()
        if not content:
            raise AIResponseError("Ollama returned an empty response.")
        return {"content": content, "provider": self.name, "model": selected_model, "raw": data}

    def list_models(self):
        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}/api/tags", timeout=20)
        except requests.RequestException as exc:
            raise AIProviderError(f"Ollama connection failed: {exc}") from exc
        if not response.ok:
            raise AIProviderError(
                f"Ollama returned HTTP {response.status_code}.")
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("Ollama returned invalid JSON.") from exc
        return [{"id": item.get("name"), "name": item.get("name"), "capabilities": ["chat"]} for item in data.get("models", []) if item.get("name")]


class OpenAIProvider(BaseAIProvider):
    name = "openai"

    def __init__(self, user=None):
        super().__init__(user)
        self.api_key = self._user_api_key() or getattr(settings, "OPENAI_API_KEY", "")
        self.base_url = getattr(
            settings, "OPENAI_BASE_URL", "https://api.openai.com/v1")
        self.default_model = getattr(settings, "OPENAI_MODEL", "gpt-4o-mini")
        if not self.api_key:
            raise AIConfigurationError(
                "OpenAI API key is not configured for this user.")

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def generate(self, messages, model=None, temperature=None, max_tokens=None):
        selected_model = model or self.default_model
        payload = {"model": selected_model, "messages": messages}
        if temperature is not None:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload["max_tokens"] = max_tokens
        try:
            response = requests.post(f"{self.base_url.rstrip('/')}/chat/completions",
                                     json=payload, headers=self._headers(), timeout=120)
        except requests.RequestException as exc:
            raise AIProviderError(f"OpenAI connection failed: {exc}") from exc
        if not response.ok:
            raise AIProviderError(
                f"OpenAI returned HTTP {response.status_code}: {response.text[:500]}")
        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise AIResponseError(
                "OpenAI returned an invalid response.") from exc
        if not content:
            raise AIResponseError("OpenAI returned an empty response.")
        return {"content": content, "provider": self.name, "model": selected_model, "raw": data}

    def list_models(self):
        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}/models", headers=self._headers(), timeout=20)
        except requests.RequestException as exc:
            raise AIProviderError(f"OpenAI connection failed: {exc}") from exc
        if not response.ok:
            raise AIProviderError(
                f"OpenAI returned HTTP {response.status_code}: {response.text[:300]}")
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("OpenAI returned invalid JSON.") from exc
        models = []
        for item in data.get("data", []):
            model_id = item.get("id")
            if model_id:
                models.append({"id": model_id, "name": model_id,
                              "capabilities": ["chat"]})
        return models


class OpenRouterProvider(OpenAIProvider):
    name = "openrouter"

    def __init__(self, user=None):
        BaseAIProvider.__init__(self, user)
        self.api_key = self._user_api_key() or getattr(
            settings, "OPENROUTER_API_KEY", "")
        self.base_url = getattr(
            settings, "OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1")
        self.default_model = getattr(
            settings, "OPENROUTER_MODEL", "openai/gpt-4o-mini")
        if not self.api_key:
            raise AIConfigurationError("OpenRouter API key is not configured.")

    def list_models(self):
        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}/models", headers=self._headers(), timeout=20)
        except requests.RequestException as exc:
            raise AIProviderError(
                f"OpenRouter connection failed: {exc}") from exc
        if not response.ok:
            raise AIProviderError(
                f"OpenRouter returned HTTP {response.status_code}: {response.text[:300]}")
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("OpenRouter returned invalid JSON.") from exc
        return [{"id": item.get("id"), "name": item.get("name") or item.get("id"), "capabilities": ["chat"]} for item in data.get("data", []) if item.get("id")]


def get_ai_provider(provider_name, user=None):
    providers = {"ollama": OllamaProvider,
                 "openai": OpenAIProvider, "openrouter": OpenRouterProvider}
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise AIConfigurationError(f"Unsupported AI provider: {provider_name}")
    return provider_class(user=user)
