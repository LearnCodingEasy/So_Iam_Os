from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from learning.models.learning_goal import LearningGoal


class LearningPath(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        PAUSED = "paused", "Paused"
        ARCHIVED = "archived", "Archived"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_paths",
    )
    goal = models.ForeignKey(
        LearningGoal,
        on_delete=models.CASCADE,
        related_name="paths",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["goal", "status"]),
        ]

    def clean(self):
        super().clean()
        if self.goal_id and self.user_id:
            if self.goal.user_id != self.user_id:
                raise ValidationError(
                    {"goal": "Goal must belong to the same user."}
                )

    def __str__(self):
        return self.title
