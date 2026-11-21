import requests
from django.conf import settings
from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError
from .base import BaseAIProvider, _provider_http_error

class GeminiProvider(BaseAIProvider):
    """Google Gemini REST API adapter using generateContent."""
    name = "gemini"

    def __init__(self, user=None):
        super().__init__(user)
        self.api_key = self._user_api_key() or getattr(settings, "GEMINI_API_KEY", "") or getattr(settings, "GOOGLE_API_KEY", "")
        self.base_url = self._validated_base_url(getattr(settings, "GEMINI_BASE_URL", "https://generativelanguage.googleapis.com/v1beta"))
        self.default_model = str(self._configured_value("model", getattr(settings, "GEMINI_MODEL", "gemini-2.5-flash"))).strip()
        if not self.api_key:
            raise AIConfigurationError("Gemini API key is not configured.")

    def generate(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):
        selected_model = model or self.default_model
        request_timeout = self._request_timeout(timeout_seconds)
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
            response = requests.post(
                url,
                headers={"x-goog-api-key": self.api_key, "Content-Type": "application/json"},
                json=payload,
                timeout=request_timeout,
            )
        except requests.Timeout as exc:
            raise AIProviderError("Gemini request timed out.", category="timeout", retryable=True) from exc
        except requests.ConnectionError as exc:
            raise AIProviderError("Gemini connection failed.", category="network_error", retryable=True) from exc
        except requests.RequestException as exc:
            raise AIProviderError("Gemini request failed.", category="network_error", retryable=True) from exc
        if not response.ok:
            # Never echo request headers, query parameters, API key, or response body.
            raise _provider_http_error(self.name, response)
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
            response = requests.get(
                url,
                headers={"x-goog-api-key": self.api_key},
                timeout=self._request_timeout(max(2, int(getattr(settings, "AI_MODEL_DISCOVERY_TIMEOUT_SECONDS", 6)))),
            )
        except requests.Timeout as exc:
            raise AIProviderError("Gemini request timed out.", category="timeout", retryable=True) from exc
        except requests.ConnectionError as exc:
            raise AIProviderError("Gemini connection failed.", category="network_error", retryable=True) from exc
        except requests.RequestException as exc:
            raise AIProviderError("Gemini request failed.", category="network_error", retryable=True) from exc
        if not response.ok:
            raise _provider_http_error(self.name, response)
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
