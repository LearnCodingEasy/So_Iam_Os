import logging

from celery import shared_task
from celery.exceptions import SoftTimeLimitExceeded

from ..services import AIService
from ..services.timeouts import celery_limits

logger = logging.getLogger(__name__)

# Celery limits always exceed the maximum AI timeout (AI_TIMEOUT_MAX_SECONDS),
# so the provider timeout fires first and produces a meaningful error; the
# Celery soft/hard limits are only a backstop against a stuck worker.
_SOFT, _HARD = celery_limits()


@shared_task(
    bind=True,
    autoretry_for=(Exception,),
    # A timeout will not get faster on retry; surface it instead of looping.
    dont_autoretry_for=(SoftTimeLimitExceeded, ValueError),
    retry_backoff=True,
    max_retries=2,
    soft_time_limit=_SOFT,
    time_limit=_HARD,
)
def generate_learning_plan(self, user_id, message, provider=None, model=None, timeout_seconds=None):
    from django.contrib.auth import get_user_model
    # Persist user ownership in Celery result metadata as soon as the worker
    # starts. The API also has a durable submission audit record for PENDING.
    self.update_state(state="STARTED", meta={"user_id": user_id})
    user = get_user_model().objects.get(pk=user_id)
    service = AIService(user)
    from ..learning_actions import AILearningActionService
    logger.info("AI learning task start task_id=%s user=%s provider=%s timeout=%s",
                self.request.id, user_id, provider or "-", timeout_seconds or "-")
    plan = AILearningActionService.generate_ai_plan(
        message=message,
        provider=provider or service.get_settings().preferred_provider,
        model=model or service.get_settings().preferred_model,
        user=user,
        timeout_seconds=timeout_seconds,
    )
    return {"user_id": user.id, "result": plan}
