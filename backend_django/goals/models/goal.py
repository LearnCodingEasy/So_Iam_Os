from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class Goal(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        PAUSED = "paused", "On Hold"
        AT_RISK = "at_risk", "At Risk"
        COMPLETED = "completed", "Completed"
        CANCELLED = "cancelled", "Cancelled"
        ARCHIVED = "archived", "Archived"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Category(models.TextChoices):
        PERSONAL = "personal", "Personal"
        PROFESSIONAL = "professional", "Professional"
        EDUCATIONAL = "educational", "Educational"
        FINANCIAL = "financial", "Financial"
        HEALTH = "health", "Health & Fitness"
        BUSINESS = "business", "Business"
        PROJECT = "project", "Project"
        OTHER = "other", "Other"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="goals")
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    category = models.CharField(max_length=24, choices=Category.choices, default=Category.PERSONAL)
    priority = models.CharField(max_length=20, choices=Priority.choices, default=Priority.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.ACTIVE)
    start_date = models.DateField(default=timezone.localdate)
    target_date = models.DateField(null=True, blank=True)
    estimated_minutes = models.PositiveIntegerField(default=0)
    actual_minutes = models.PositiveIntegerField(default=0)
    progress_percent = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    measurement_unit = models.CharField(max_length=40, blank=True)
    initial_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    target_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    current_value = models.DecimalField(max_digits=14, decimal_places=2, null=True, blank=True)
    completion_notes = models.TextField(blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    learning_goals = models.ManyToManyField("learning.LearningGoal", blank=True, related_name="general_goals")
    skills = models.ManyToManyField("learning.Skill", blank=True, related_name="goals")
    related_goals = models.ManyToManyField("self", blank=True, symmetrical=False, related_name="related_to")

    class Meta:
        ordering = ["-priority", "target_date", "-created_at"]
        indexes = [
            models.Index(fields=["user", "status"]),
            models.Index(fields=["user", "target_date"]),
            models.Index(fields=["user", "priority"]),
            models.Index(fields=["user", "category", "status"]),
        ]

    def __str__(self):
        return self.title

    def mark_completed(self):
        self.status = self.Status.COMPLETED
        self.progress_percent = 100
        self.completed_at = self.completed_at or timezone.now()
        self.save(update_fields=["status", "progress_percent", "completed_at", "updated_at"])
