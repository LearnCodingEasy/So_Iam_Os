from celery import shared_task
from django.contrib.auth import get_user_model
from .daily_generation import DailyTaskGenerationService

@shared_task(bind=True, autoretry_for=(Exception,), retry_backoff=True, max_retries=2)
def generate_daily_learning_tasks(self, user_id, count=None, provider=None, model=None):
    user = get_user_model().objects.get(pk=user_id)
    tasks = DailyTaskGenerationService(user).generate(count=count, provider=provider, model=model)
    return {"created": len(tasks), "task_ids": [t.id for t in tasks]}

@shared_task
def generate_daily_learning_tasks_for_all_users():
    User = get_user_model()
    created = 0
    for user in User.objects.filter(is_active=True):
        created += len(DailyTaskGenerationService(user).generate())
    return {"created": created}
