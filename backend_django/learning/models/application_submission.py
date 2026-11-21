from django.db import models
from django.utils import timezone
from learning.models.knowledge_application import KnowledgeApplication


class ApplicationSubmission(models.Model):
    """Immutable snapshot of an application submitted for review."""

    application = models.ForeignKey(
        KnowledgeApplication,
        on_delete=models.CASCADE,
        related_name="submissions",
    )
    version = models.PositiveIntegerField()
    title = models.CharField(max_length=255)
    content = models.TextField()
    submitted_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ["-version"]
        constraints = [
            models.UniqueConstraint(
                fields=["application", "version"],
                name="unique_application_submission_version",
            ),
        ]

    def __str__(self):
        return f"{self.application} v{self.version}"
