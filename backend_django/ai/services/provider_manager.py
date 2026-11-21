"""Provider capability and credential-safe management."""
from django.conf import settings
from ..models import AIProviderCredential, AISettings
from ..providers import get_ai_provider

class ProviderManager:
    SUPPORTED = ("ollama", "openai", "gemini", "deepseek", "openrouter")
    @classmethod
    def list_for_user(cls, user):
        result = []
        preferences = AISettings.objects.filter(user=user).first()
        default_provider = (preferences.preferred_provider if preferences else None) or getattr(settings, "AI_DEFAULT_PROVIDER", "ollama")
        credentials = {
            row.provider: row
            for row in AIProviderCredential.objects.filter(user=user, provider__in=cls.SUPPORTED)
        }
        for name in cls.SUPPORTED:
            credential = credentials.get(name)
            metadata = dict((credential.metadata if credential else {}) or {})
            result.append({
                "provider": name,
                "has_api_key": bool(credential and credential.has_api_key),
                "is_default": name == default_provider,
                "enabled": metadata.get("enabled", True),
                "priority": metadata.get("priority", 100),
                "base_url": metadata.get("base_url", ""),
                "model": metadata.get("model", ""),
            })
        return result
    @staticmethod
    def list_models(*, user, provider):
        return get_ai_provider(provider, user=user).list_models()
