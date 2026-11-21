from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class LocalAIJob(models.Model):
    STATUS_CHOICES = [
        ("queued", "Queued"),
        ("running", "Running"),
        ("completed", "Completed"),
        ("failed", "Failed"),
        ("cancelled", "Cancelled"),
    ]
    TASK_CHOICES = [
        ("summarize", "Summarize"),
        ("classify", "Classify"),
        ("metadata", "Metadata"),
        ("markdown_index", "Markdown Index"),
        ("architecture", "Architecture"),
    ]
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="local_ai_jobs")
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    task_type = models.CharField(
        max_length=40, choices=TASK_CHOICES, default="metadata")
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="queued")
    input_data = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    provider = models.CharField(max_length=80, default="local")
    error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-created_at"]
