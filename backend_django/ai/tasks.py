from celery import shared_task
from .services import AIService

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def generate_learning_plan(self, user_id, message, provider=None, model=None):
    from django.contrib.auth import get_user_model
    user = get_user_model().objects.get(pk=user_id)
    service = AIService(user)
    from .learning_actions import AILearningActionService
    plan = AILearningActionService.generate_ai_plan(message=message, provider=provider or service.get_settings().preferred_provider, model=model or service.get_settings().preferred_model, user=user)
    return plan
