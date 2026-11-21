from django.conf import settings
from django.db import models
from learning.models.skill import Skill


class LearningGoal(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        COMPLETED = "completed", "Completed"
        PAUSED = "paused", "Paused"
        ARCHIVED = "archived", "Archived"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_goals",
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="learning_goals",
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    reason = models.TextField(blank=True)

    current_level = models.CharField(
        max_length=20,
        choices=Skill.Level.choices,
        blank=True,
    )
    target_level = models.CharField(
        max_length=20,
        choices=Skill.Level.choices,
        default=Skill.Level.INTERMEDIATE,
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.ACTIVE,
    )
    target_date = models.DateField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "target_date"]),
        ]

    def __str__(self):
        return self.title
