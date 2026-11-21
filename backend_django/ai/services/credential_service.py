from django.utils import timezone
from ..models import AIProviderCredential
from ..providers import get_ai_provider

class CredentialService:
    def __init__(self,user): self.user=user
    def save(self,provider,api_key,metadata=None):
        obj,_=AIProviderCredential.objects.get_or_create(user=self.user,provider=provider)
        obj.set_api_key(api_key); obj.metadata=metadata or {}; obj.status='needs_review'; obj.save()
        return obj
    def validate(self,provider,model=''):
        obj=AIProviderCredential.objects.filter(user=self.user,provider=provider).first()
        if not obj or not obj.has_api_key: return {'valid':False,'status':'needs_review','error':'Credential is missing.'}
        try:
            result=get_ai_provider(provider,user=self.user).health_check(); valid=bool(result.get('healthy'))
        except Exception as exc:
            valid=False; result={'healthy':False,'error':str(exc)}
        obj.status='valid' if valid else 'invalid'; obj.last_validated_at=timezone.now(); obj.save(update_fields=['status','last_validated_at','updated_at'])
        return {'valid':valid,'status':obj.status,'provider':provider,'details':result}
