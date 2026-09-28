import uuid

from django.conf import settings
from django.db import models


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
        ordering = ["-created_at"]
    def __str__(self):
        return str(self.id)


class UserLearningSettings(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="learning_settings")
    daily_learning_tasks = models.PositiveSmallIntegerField(default=5)
    current_learning_goal = models.ForeignKey(
        "learning.LearningGoal", null=True, blank=True, on_delete=models.SET_NULL, related_name="focused_by_users"
    )
    task_generation_enabled = models.BooleanField(default=True)
    preferred_learning_time = models.TimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.CheckConstraint(condition=models.Q(daily_learning_tasks__gte=1) & models.Q(daily_learning_tasks__lte=10), name="learning_tasks_1_10")]

    def clean(self):
        if self.current_learning_goal_id and self.current_learning_goal.user_id != self.user_id:
            from django.core.exceptions import ValidationError
            raise ValidationError({"current_learning_goal": "The learning goal must belong to the same user."})
