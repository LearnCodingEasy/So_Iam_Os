
from django.conf import settings
from django.db import models


class AIWorkflowDefinition(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_workflows"
    )

    name = models.CharField(max_length=160)
    description = models.TextField(blank=True, default="")
    graph = models.JSONField(default=dict)

    version = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    schema_version = models.CharField(max_length=32, default="1.0")

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "name", "version"],
                name="unique_ai_workflow_version"
            )
        ]
        indexes = [
            models.Index(fields=["user", "-updated_at"])
        ]

    def __str__(self):
        return f"{self.name} (v{self.version})"


class AIWorkflowRun(models.Model):

    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_workflow_runs"
    )

    workflow = models.ForeignKey(
        "ai.AIWorkflowDefinition",
        on_delete=models.CASCADE,
        related_name="runs"
    )

    execution = models.ForeignKey(
        "ai.AIExecution",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="workflow_runs"
    )

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.QUEUED
    )

    workflow_version = models.PositiveIntegerField(default=1)
    current_node_id = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    retry_count = models.PositiveSmallIntegerField(default=0)

    input_data = models.JSONField(default=dict, blank=True)
    output_data = models.JSONField(default=dict, blank=True)

    error = models.TextField(blank=True, default="")

    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["workflow", "-created_at"]),
        ]

    def __str__(self):
        return f"Workflow Run #{self.pk} - {self.status}"
