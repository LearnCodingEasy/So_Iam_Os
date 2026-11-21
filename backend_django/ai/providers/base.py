import ipaddress
from urllib.parse import urlsplit

import requests

from django.conf import settings
from django.utils import timezone

from ..exceptions import AIConfigurationError, AIProviderError, AIResponseError
from ..models import AIProviderCredential


def _provider_http_error(provider, response):
    """Convert HTTP failures into safe, typed errors without echoing provider bodies."""
    status_code = int(getattr(response, "status_code", 0) or 0)
    retry_after = getattr(response, "headers", {}).get("Retry-After")
    try:
        retry_after = max(0, min(300, int(retry_after))) if retry_after else None
    except (TypeError, ValueError):
        retry_after = None

    if status_code in (401, 403):
        return AIProviderError(
            f"{provider} authentication/permission failed (HTTP {status_code}).",
            category="authentication", retryable=False, status_code=status_code,
        )
    if status_code == 429:
        # Providers commonly use 429 for both transient throttling and
        # permanent quota/billing exhaustion. Only the former is retryable.
        error_code = ""
        try:
            body = response.json() or {}
            error = body.get("error") or {}
            error_code = str(error.get("code") or "").lower()
        except Exception:
            pass
        quota_codes = {"insufficient_quota", "billing_hard_limit_reached", "quota_exceeded", "payment_required"}
        if error_code in quota_codes:
            return AIProviderError(
                f"{provider} quota or billing limit has been exhausted.",
                category="quota_exhausted", retryable=False, status_code=status_code,
            )
        return AIProviderError(
            f"{provider} rate limit reached (HTTP 429).",
            category="rate_limit", retryable=True, status_code=status_code,
            retry_after=retry_after,
        )
    if status_code in (408, 425) or status_code >= 500:
        return AIProviderError(
            f"{provider} temporary server failure (HTTP {status_code}).",
            category="temporary_server_error", retryable=True, status_code=status_code,
            retry_after=retry_after,
        )
    if status_code in (400, 404, 405, 413, 422):
        return AIProviderError(
            f"{provider} rejected the request (HTTP {status_code}).",
            category="invalid_request_or_model", retryable=False, status_code=status_code,
        )
    return AIProviderError(
        f"{provider} returned HTTP {status_code}.",
        category="provider_error", retryable=False, status_code=status_code,
    )



class BaseAIProvider:
    name = None

    def __init__(self, user=None):
        self.user = user
        self.credential = None
        self.metadata = {}
        if user is not None and getattr(user, "is_authenticated", False):
            self.credential = AIProviderCredential.objects.filter(
                user=user, provider=self.name
            ).first()
            if self.credential:
                self.metadata = dict(self.credential.metadata or {})

    def _configured_value(self, key, default=None):
        value = self.metadata.get(key)
        return value if value not in (None, "") else default

    def _validated_base_url(self, default):
        """Validate provider endpoints before making outbound requests."""
        raw = str(self._configured_value("base_url", default) or "").strip()
        try:
            parsed = urlsplit(raw)
            hostname = parsed.hostname
            # Accessing .port also validates malformed/out-of-range ports.
            _ = parsed.port
        except ValueError as exc:
            raise AIConfigurationError("The configured provider URL is invalid.") from exc

        if (
            parsed.scheme not in {"http", "https"}
            or not hostname
            or parsed.username
            or parsed.password
            or parsed.query
            or parsed.fragment
        ):
            raise AIConfigurationError(
                "Provider URLs must use HTTP(S), include a host, and contain no credentials, query, or fragment."
            )

        if getattr(settings, "ENVIRONMENT", "local") == "production" and self.name != "ollama":
            if parsed.scheme != "https":
                raise AIConfigurationError("External AI provider URLs must use HTTPS in production.")
            try:
                address = ipaddress.ip_address(hostname)
            except ValueError:
                address = None
            if address and (
                address.is_private or address.is_loopback or address.is_link_local
                or address.is_multicast or address.is_unspecified
            ):
                raise AIConfigurationError(
                    "External AI provider URLs cannot target private or local IP addresses in production."
                )

        return raw.rstrip("/")

    def _request_timeout(self, timeout_seconds=None):
        total = max(1, int(timeout_seconds or getattr(settings, "AI_PROVIDER_TIMEOUT_SECONDS", 35)))
        connect = max(1, min(total, int(getattr(settings, "AI_PROVIDER_CONNECT_TIMEOUT_SECONDS", 5))))
        read = max(1, total)
        return (connect, read)

    def generate(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):
        raise NotImplementedError

    def list_models(self):
        raise NotImplementedError

    def generate_stream(self, messages, model=None, temperature=None, max_tokens=None, timeout_seconds=None):
        # Safe compatibility fallback: providers can override with native streaming.
        result = self.generate(messages, model=model, temperature=temperature, max_tokens=max_tokens, timeout_seconds=timeout_seconds)
        yield result

    def validate_credentials(self):
        self.list_models()
        return True

    def health_check(self):
        try:
            self.list_models()
            return {"healthy": True, "provider": self.name}
        except Exception as exc:
            return {"healthy": False, "provider": self.name, "error": str(exc)}

    def get_model_info(self, model):
        for item in self.list_models():
            if item.get("id") == model:
                return item
        return None

    def estimate_tokens(self, messages):
        text = " ".join(str(item.get("content") or "") for item in messages if isinstance(item, dict))
        return max(1, (len(text) + 3) // 4)

    def calculate_cost(self, *, input_tokens=0, output_tokens=0, model=None):
        # Provider-specific pricing can override this; never invent a cost.
        return None

    def _user_api_key(self):
        if not self.credential or not self.credential.has_api_key:
            return ""
        try:
            self.credential.last_used_at = timezone.now()
            self.credential.save(update_fields=["last_used_at", "updated_at"])
            return (self.credential.get_api_key() or "").strip()
        except (ValueError, TypeError) as exc:
            raise AIConfigurationError(
                f"The saved {self.name} credential cannot be decrypted. Please replace it in AI settings."
            ) from exc
