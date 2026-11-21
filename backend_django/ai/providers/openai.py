import requests
from django.conf import settings
from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError
from .base import BaseAIProvider, _provider_http_error

class OpenAIProvider(BaseAIProvider):
    name = "openai"

    def __init__(self, user=None):
        super().__init__(user)
        self.api_key = self._user_api_key() or getattr(settings, "OPENAI_API_KEY", "")
        self.base_url = self._validated_base_url(getattr(settings, "OPENAI_BASE_URL", "https://api.openai.com/v1"))
        self.default_model = str(self._configured_value("model", getattr(settings, "OPENAI_MODEL", "gpt-4o-mini"))).strip()

        if not self.api_key:
            raise AIConfigurationError(
                "OpenAI API key is not configured for this user.")

    def _headers(self):
        return {"Authorization": f"Bearer {self.api_key}", "Content-Type": "application/json"}

    def generate(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):
        selected_model = model or self.default_model
        request_timeout = self._request_timeout(timeout_seconds)
        payload = {"model": selected_model, "messages": messages}
        # Reasoning/new-generation model families use the completion-token
        # parameter and may reject sampling controls such as temperature.
        normalized_model = selected_model.lower()
        uses_completion_tokens = (
            normalized_model.startswith(("o1", "o3", "o4", "gpt-5", "gpt-6"))
        )
        if temperature is not None and not uses_completion_tokens:
            payload["temperature"] = temperature
        if max_tokens is not None:
            payload[
                "max_completion_tokens" if uses_completion_tokens else "max_tokens"
            ] = max_tokens
        try:
            response = requests.post(f"{self.base_url.rstrip('/')}/chat/completions",
                                     json=payload, headers=self._headers(), allow_redirects=False,
                                     timeout=request_timeout)
        except requests.Timeout as exc:
            raise AIProviderError(f"{self.name} request timed out.", category="timeout", retryable=True) from exc
        except requests.ConnectionError as exc:
            raise AIProviderError(f"{self.name} connection failed.", category="network_error", retryable=True) from exc
        except requests.RequestException as exc:
            raise AIProviderError(f"{self.name} request failed.", category="network_error", retryable=True) from exc
        if not response.ok:
            raise _provider_http_error(self.name, response)
        try:
            data = response.json()
            content = data["choices"][0]["message"]["content"].strip()
        except (ValueError, KeyError, IndexError, TypeError) as exc:
            raise AIResponseError(
                f"{self.name} returned an invalid response.") from exc
        if not content:
            raise AIResponseError("OpenAI returned an empty response.")
        return {"content": content, "provider": self.name, "model": selected_model, "raw": data}

    def generate_stream(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):
        selected_model=model or self.default_model
        timeout=self._request_timeout(timeout_seconds)
        payload={"model":selected_model,"messages":messages,"stream":True}
        normalized=selected_model.lower(); reasoning=normalized.startswith(("o1","o3","o4","gpt-5","gpt-6"))
        if temperature is not None and not reasoning: payload["temperature"]=temperature
        if max_tokens is not None: payload["max_completion_tokens" if reasoning else "max_tokens"]=max_tokens
        try: response=requests.post(f"{self.base_url.rstrip('/')}/chat/completions",json=payload,headers=self._headers(),stream=True,timeout=timeout)
        except requests.Timeout as exc: raise AIProviderError(f"{self.name} request timed out.",category="timeout",retryable=True) from exc
        except requests.RequestException as exc: raise AIProviderError(f"{self.name} connection failed.",category="network_error",retryable=True) from exc
        if not response.ok: raise _provider_http_error(self.name,response)
        import json
        try:
            for line in response.iter_lines(decode_unicode=True):
                if not line or not line.startswith("data:"):
                    continue
                raw = line[5:].strip()
                if raw == "[DONE]":
                    yield {"delta": "", "content": "", "provider": self.name,
                           "model": selected_model, "done": True}
                    break
                try:
                    data = json.loads(raw)
                except (TypeError, ValueError):
                    continue
                choice = (data.get("choices") or [{}])[0]
                delta = ((choice.get("delta") or {}).get("content") or "")
                if delta:
                    yield {"delta": delta, "content": delta, "provider": self.name,
                           "model": selected_model, "done": False}
        finally:
            response.close()

    def list_models(self):
        try:
            response = requests.get(
                f"{self.base_url.rstrip('/')}/models", headers=self._headers(),
                allow_redirects=False,
                timeout=self._request_timeout(max(2, int(getattr(settings, "AI_MODEL_DISCOVERY_TIMEOUT_SECONDS", 6)))),
            )
        except requests.RequestException as exc:
            raise AIProviderError(f"{self.name} connection failed.") from exc
        if not response.ok:
            raise _provider_http_error(self.name, response)
        try:
            data = response.json()
        except ValueError as exc:
            raise AIResponseError(f"{self.name} returned invalid JSON.") from exc
        models = []
        for item in data.get("data", []):
            model_id = item.get("id")
            if model_id:
                models.append({"id": model_id, "name": model_id,
                              "capabilities": ["chat"]})
        return models



