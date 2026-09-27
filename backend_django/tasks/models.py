from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Task(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        POSTPONED = "postponed", "Postponed"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, related_name="tasks")
    goal = models.ForeignKey("goals.Goal", on_delete=models.SET_NULL,
                             null=True, blank=True, related_name="tasks")
    learning_goal = models.ForeignKey(
        "learning.LearningGoal", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    learning_path = models.ForeignKey(
        "learning.LearningPath", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    learning_topic = models.ForeignKey(
        "learning.LearningTopic", on_delete=models.SET_NULL, null=True, blank=True, related_name="tasks")
    skill = models.ForeignKey("learning.Skill", on_delete=models.SET_NULL,
                              null=True, blank=True, related_name="tasks")

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    scheduled_date = models.DateField(default=timezone.localdate)
    scheduled_start = models.TimeField(null=True, blank=True)
    due_at = models.DateTimeField(null=True, blank=True)
    estimated_minutes = models.PositiveIntegerField(default=0)
    actual_minutes = models.PositiveIntegerField(default=0)
    priority = models.CharField(
        max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.PENDING)
    sort_order = models.PositiveIntegerField(default=0)
    completed_at = models.DateTimeField(null=True, blank=True)
    postponed_until = models.DateField(null=True, blank=True)
    recurrence_rule = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_date", "sort_order",
                    "-priority", "scheduled_start", "created_at"]
        indexes = [
            models.Index(fields=["user", "scheduled_date", "status"]),
            models.Index(fields=["user", "priority"]),
            models.Index(fields=["goal", "status"]),
            models.Index(fields=["learning_topic", "status"]),
        ]

    def __str__(self):
        return self.title

    def mark_completed(self):
        self.status = self.Status.COMPLETED
        self.completed_at = self.completed_at or timezone.now()
        self.save(update_fields=["status", "completed_at", "updated_at"])
