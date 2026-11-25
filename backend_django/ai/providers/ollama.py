import requests
from django.conf import settings
from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError
from .base import BaseAIProvider, _provider_http_error


def _timeout_error(exc, timeouts):
    """Build a meaningful timeout error that separates connect vs read timeouts."""
    connect, read = timeouts
    if isinstance(exc, requests.ConnectTimeout):
        error = AIProviderError(
            f"Could not connect to Ollama within {connect}s (connection timeout). "
            "Check that the Ollama service is running and reachable.",
            category="timeout", retryable=True)
        error.timeout_kind = "connect"
    else:
        error = AIProviderError(
            f"Ollama accepted the request but did not finish within {read}s (read timeout). "
            "The model may still be loading into memory; retry or raise the timeout.",
            category="timeout", retryable=True)
        error.timeout_kind = "read"
    return error

class OllamaProvider(BaseAIProvider):
    name = "ollama"

    def __init__(self, user=None):
        super().__init__(user)
        self.base_url = self._validated_base_url(getattr(settings, "OLLAMA_BASE_URL", "http://127.0.0.1:11434"))
        self.default_model = str(self._configured_value("model", getattr(settings, "OLLAMA_MODEL", "gemma3:4b"))).strip()
        self.auth_token = str(self._configured_value("auth_token", "")).strip()


    def generate(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):
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
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        try:
            response = requests.post(
                f"{self.base_url.rstrip('/')}/api/chat", json=payload, headers=headers, timeout=self._request_timeout(timeout_seconds))
        except requests.Timeout as exc:
            raise _timeout_error(exc, self._request_timeout(timeout_seconds)) from exc
        except requests.ConnectionError as exc:
            raise AIProviderError("Ollama connection failed.", category="network_error", retryable=True) from exc
        except requests.RequestException as exc:
            raise AIProviderError("Ollama connection failed.", category="network_error", retryable=True) from exc
        if not response.ok:
            raise _provider_http_error(self.name, response)
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("Ollama returned invalid JSON.") from exc
        content = data.get("message", {}).get("content", "").strip()
        if not content:
            raise AIResponseError("Ollama returned an empty response.")
        return {"content": content, "provider": self.name, "model": selected_model, "raw": data}

    def generate_stream(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):
        import json

        selected_model = model or self.default_model
        payload = {"model": selected_model, "messages": messages, "stream": True}
        options = {}
        if temperature is not None:
            options["temperature"] = temperature
        if max_tokens is not None:
            options["num_predict"] = max_tokens
        if options:
            payload["options"] = options
        headers = {"Authorization": f"Bearer {self.auth_token}"} if self.auth_token else {}
        try:
            response = requests.post(
                f"{self.base_url.rstrip('/')}/api/chat",
                json=payload,
                headers=headers,
                stream=True,
                timeout=self._request_timeout(timeout_seconds),
            )
        except requests.Timeout as exc:
            raise _timeout_error(exc, self._request_timeout(timeout_seconds)) from exc
        except requests.RequestException as exc:
            raise AIProviderError("Ollama connection failed.", category="network_error", retryable=True) from exc
        if not response.ok:
            raise _provider_http_error(self.name, response)
        try:
            for line in response.iter_lines(decode_unicode=True):
                if not line:
                    continue
                try:
                    data = json.loads(line)
                except (TypeError, ValueError):
                    continue
                delta = ((data.get("message") or {}).get("content") or "")
                if delta:
                    yield {"delta": delta, "content": delta, "provider": self.name,
                           "model": selected_model, "done": False}
                if data.get("done"):
                    yield {"delta": "", "content": "", "provider": self.name,
                           "model": selected_model, "done": True}
                    break
        finally:
            response.close()

    def list_models(self):
        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}/api/tags", timeout=self._request_timeout(max(2, int(getattr(settings, "AI_MODEL_DISCOVERY_TIMEOUT_SECONDS", 6)))))
        except requests.Timeout as exc:
            raise AIProviderError("Ollama model discovery timed out.", category="timeout", retryable=True) from exc
        except requests.ConnectionError as exc:
            raise AIProviderError("Ollama model discovery failed.", category="network_error", retryable=True) from exc
        except requests.RequestException as exc:
            raise AIProviderError("Ollama model discovery failed.", category="network_error", retryable=True) from exc
        if not response.ok:
            raise _provider_http_error(self.name, response)
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError("Ollama returned invalid JSON.") from exc
        return [{"id": item.get("name"), "name": item.get("name"), "capabilities": ["chat"]} for item in data.get("models", []) if item.get("name")]



