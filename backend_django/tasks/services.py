from django.db import transaction
from django.utils import timezone

from .models import Task


class TaskService:
    @staticmethod
    @transaction.atomic
    def complete(task, actual_minutes=None):
        task.status = Task.Status.COMPLETED
        task.completed_at = task.completed_at or timezone.now()
        if actual_minutes is not None:
            task.actual_minutes = max(0, int(actual_minutes))
        task.save(update_fields=["status", "completed_at", "actual_minutes", "updated_at"])
        return task

    @staticmethod
    def postpone(task, until):
        task.status = Task.Status.POSTPONED
        task.postponed_until = until
        task.scheduled_date = until
        task.save(update_fields=["status", "postponed_until", "scheduled_date", "updated_at"])
        return task
