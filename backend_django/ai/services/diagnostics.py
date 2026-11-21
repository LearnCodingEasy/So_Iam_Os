from django.db import connection
from django.conf import settings
from .provider_service import ProviderService

class AIDiagnostics:
    def __init__(self,user): self.user=user
    def run(self):
        checks={}
        try:
            connection.ensure_connection(); checks["database"]={"ok":True}
        except Exception as exc: checks["database"]={"ok":False,"error":str(exc)}
        checks["auth"]={"ok":bool(self.user and self.user.is_authenticated)}
        providers={}
        for name in ["ollama","openai","gemini","deepseek","openrouter"]:
            try: providers[name]=ProviderService(self.user).health(name)
            except Exception as exc: providers[name]={"healthy":False,"provider":name,"error":str(exc)}
        checks["providers"]=providers
        checks["api_default_provider"]={"ok":bool(getattr(settings,"AI_DEFAULT_PROVIDER","")),"value":getattr(settings,"AI_DEFAULT_PROVIDER","")}
        return {"ok":checks["database"]["ok"] and checks["auth"]["ok"],"checks":checks}
