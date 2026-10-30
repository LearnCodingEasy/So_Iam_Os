import requests

from django.conf import settings

from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError
from ..models import AIProviderCredential


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
                f"{self.base_url.rstrip('/')}/api/chat", json=payload, timeout=max(5, int(getattr(settings, "AI_PROVIDER_TIMEOUT_SECONDS", 35))))
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
                                     json=payload, headers=self._headers(), timeout=max(5, int(getattr(settings, "AI_PROVIDER_TIMEOUT_SECONDS", 35))))
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



class DeepSeekProvider(OpenAIProvider):
    """DeepSeek exposes an OpenAI-compatible Chat Completions API."""
    name = "deepseek"

    def __init__(self, user=None):
        BaseAIProvider.__init__(self, user)
        self.api_key = self._user_api_key() or getattr(settings, "DEEPSEEK_API_KEY", "")
        self.base_url = getattr(settings, "DEEPSEEK_BASE_URL", "https://api.deepseek.com")
        self.default_model = getattr(settings, "DEEPSEEK_MODEL", "deepseek-chat")
        if not self.api_key:
            raise AIConfigurationError("DeepSeek API key is not configured.")

    def list_models(self):
        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}/models",
                headers=self._headers(), timeout=20,
            )
        except requests.RequestException as exc:
            raise AIProviderError(f"DeepSeek connection failed: {exc}") from exc
        if not response.ok:
            raise AIProviderError(f"DeepSeek returned HTTP {response.status_code}.")
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("DeepSeek returned invalid JSON.") from exc
        return [
            {"id": item.get("id"), "name": item.get("id"), "capabilities": ["chat"]}
            for item in data.get("data", []) if item.get("id")
        ]


class GeminiProvider(BaseAIProvider):
    """Google Gemini REST API adapter using generateContent."""
    name = "gemini"

    def __init__(self, user=None):
        super().__init__(user)
        self.api_key = self._user_api_key() or getattr(settings, "GEMINI_API_KEY", "") or getattr(settings, "GOOGLE_API_KEY", "")
        self.base_url = getattr(settings, "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta")
        self.default_model = getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash")
        if not self.api_key:
            raise AIConfigurationError("Gemini API key is not configured.")

    def generate(self, messages, model=None, temperature=None, max_tokens=None):
        selected_model = model or self.default_model
        system_parts, contents = [], []
        for item in messages:
            role = item.get("role", "user")
            content = str(item.get("content", ""))
            if role == "system":
                system_parts.append(content)
            elif content:
                contents.append({"role": "model" if role == "assistant" else "user",
                                 "parts": [{"text": content}]})
        if system_parts:
            # Gemini supports system_instruction in the generateContent request.
            payload = {"system_instruction": {"parts": [{"text": "\n\n".join(system_parts)}]},
                       "contents": contents}
        else:
            payload = {"contents": contents}
        generation_config = {}
        if temperature is not None:
            generation_config["temperature"] = temperature
        if max_tokens is not None:
            generation_config["maxOutputTokens"] = max_tokens
        if generation_config:
            payload["generationConfig"] = generation_config
        url = f"{self.base_url.rstrip('/')}/models/{selected_model}:generateContent"
        try:
            response = requests.post(url, params={"key": self.api_key}, json=payload, timeout=max(5, int(getattr(settings, "AI_PROVIDER_TIMEOUT_SECONDS", 35))))
        except requests.RequestException as exc:
            raise AIProviderError("Gemini connection failed.") from exc
        if not response.ok:
            # Never echo request headers or API key; response body may include user data.
            raise AIProviderError(f"Gemini returned HTTP {response.status_code}.")
        try:
            data = response.json()
            content = "".join(part.get("text", "") for part in
                              data["candidates"][0]["content"]["parts"]).strip()
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise AIResponseError("Gemini returned an invalid response.") from exc
        if not content:
            raise AIResponseError("Gemini returned an empty response.")
        return {"content": content, "provider": self.name, "model": selected_model, "raw": data}

    def list_models(self):
        url = f"{self.base_url.rstrip('/')}/models"
        try:
            response = requests.get(url, params={"key": self.api_key}, timeout=20)
        except requests.RequestException as exc:
            raise AIProviderError("Gemini connection failed.") from exc
        if not response.ok:
            raise AIProviderError(f"Gemini returned HTTP {response.status_code}.")
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("Gemini returned invalid JSON.") from exc
        models = []
        for item in data.get("models", []):
            name = item.get("name", "").replace("models/", "")
            methods = item.get("supportedGenerationMethods", [])
            if name and "generateContent" in methods:
                models.append({"id": name, "name": name, "capabilities": ["chat"]})
        return models


def get_ai_provider(provider_name, user=None):
    providers = {"ollama": OllamaProvider, "openai": OpenAIProvider,
                 "openrouter": OpenRouterProvider, "gemini": GeminiProvider,
                 "deepseek": DeepSeekProvider}
    provider_class = providers.get(provider_name)
    if not provider_class:
        raise AIConfigurationError(f"Unsupported AI provider: {provider_name}")
    return provider_class(user=user)
