from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from learning.models.application_review import ApplicationReview
from learning.models.learning_topic import LearningTopic


class LearningRevision(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        IN_PROGRESS = "in_progress", "In Progress"
        COMPLETED = "completed", "Completed"
        SKIPPED = "skipped", "Skipped"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_revisions",
    )
    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="revisions",
    )
    source_review = models.ForeignKey(
        ApplicationReview,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="revision_sessions",
    )

    concepts = models.JSONField(default=list, blank=True)
    recommendation = models.TextField(blank=True)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PLANNED,
    )
    scheduled_for = models.DateTimeField(null=True, blank=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    outcome = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_for", "-created_at"]
        indexes = [
            models.Index(fields=["user", "status", "scheduled_for"]),
        ]

    def clean(self):
        super().clean()
        if self.completed_at and self.started_at:
            if self.completed_at < self.started_at:
                raise ValidationError(
                    {"completed_at": "Cannot precede start time."}
                )

    def __str__(self):
        return f"Revision: {self.topic} - {self.user}"
