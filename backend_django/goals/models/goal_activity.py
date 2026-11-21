from django.conf import settings
from django.db import models
from goals.models.goal import Goal


class GoalActivity(models.Model):
    goal = models.ForeignKey(Goal, on_delete=models.CASCADE, related_name="activity")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goal_activity")
    event_type = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    data = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["goal", "created_at"])]
