"""Provider orchestration: selection, health, discovery and safe fallback."""
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from ..providers import get_ai_provider
from ..exceptions import AIConfigurationError, AIProviderError

HEALTH_TTL = 30
MODELS_TTL = 120

class ProviderService:
    def __init__(self, user):
        self.user = user

    def provider(self, name):
        return get_ai_provider(name, user=self.user)

    def health(self, name, force=False):
        key=f"ai:health:{self.user.pk}:{name}"
        if not force:
            cached=cache.get(key)
            if cached is not None:
                return cached
        try:
            result=self.provider(name).health_check()
        except Exception as exc:
            result={"healthy":False,"provider":name,"error":str(exc)}
        result["checked_at"]=timezone.now().isoformat()
        cache.set(key,result,HEALTH_TTL)
        return result

    def models(self, name, force=False):
        key=f"ai:models:{self.user.pk}:{name}"
        if not force:
            cached=cache.get(key)
            if cached is not None:
                return cached
        result=self.provider(name).list_models()
        cache.set(key,result,MODELS_TTL)
        return result

    def test(self, name, model=""):
        provider=self.provider(name)
        selected=model or getattr(provider,"default_model","")
        messages=[{"role":"user","content":"Reply with exactly: AI_CONNECTION_OK"}]
        result=provider.generate(messages,model=selected,temperature=0,max_tokens=32,timeout_seconds=10)
        return {"ok":bool(result.get("content")),"provider":result.get("provider"),"model":result.get("model"),"content":result.get("content","")}
