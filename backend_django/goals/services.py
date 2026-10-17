from django.db import transaction
from django.utils import timezone

from .models import Goal


class GoalService:
    @staticmethod
    @transaction.atomic
    def complete(goal, notes=""):
        goal.status = Goal.Status.COMPLETED
        goal.progress_percent = 100
        goal.completed_at = goal.completed_at or timezone.now()
        if notes:
            goal.completion_notes = notes
        goal.save(update_fields=["status", "progress_percent",
                  "completed_at", "completion_notes", "updated_at"])
        return goal

    @staticmethod
    @transaction.atomic
    def recalculate_from_tasks(goal):
        """Recompute goal progress from its actual task completion state."""
        total = goal.tasks.count()
        if total == 0 or goal.status in {Goal.Status.CANCELLED, Goal.Status.ARCHIVED}:
            return goal
        completed = goal.tasks.filter(status="completed").count()
        progress = round((completed / total) * 100)
        goal.progress_percent = max(0, min(100, progress))
        if progress == 100:
            goal.status = Goal.Status.COMPLETED
            goal.completed_at = goal.completed_at or timezone.now()
        elif goal.status == Goal.Status.COMPLETED:
            goal.status = Goal.Status.ACTIVE
            goal.completed_at = None
        goal.save(update_fields=["progress_percent", "status", "completed_at", "updated_at"])
        return goal

    @staticmethod
    def update_progress(goal, progress):
        goal.progress_percent = max(0, min(100, int(progress)))
        if goal.progress_percent == 100:
            goal.status = Goal.Status.COMPLETED
            goal.completed_at = goal.completed_at or timezone.now()
        elif goal.status == Goal.Status.COMPLETED:
            goal.status = Goal.Status.ACTIVE
            goal.completed_at = None
        goal.save(update_fields=["progress_percent",
                  "status", "completed_at", "updated_at"])
        return goal
