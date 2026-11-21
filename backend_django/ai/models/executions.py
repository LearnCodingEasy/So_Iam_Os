from django.conf import settings
from django.db import models
from .conversations import AIConversation
from ..security import decrypt_secret, encrypt_secret

class AIExecution(models.Model):
    class Status(models.TextChoices):
        QUEUED = "queued", "Queued"
        RUNNING = "running", "Running"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        CANCELLED = "cancelled", "Cancelled"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="ai_executions")
    conversation = models.ForeignKey(
        AIConversation, on_delete=models.SET_NULL, null=True, blank=True, related_name="executions")
    agent = models.CharField(max_length=120, default="default")
    task_type = models.CharField(max_length=80, default="chat")
    requested_provider = models.CharField(
        max_length=50, blank=True, default="")
    provider = models.CharField(max_length=50, blank=True, default="")
    model = models.CharField(max_length=255, blank=True, default="")
    status = models.CharField(
        max_length=20, choices=Status.choices, default=Status.QUEUED)
    started_at = models.DateTimeField(null=True, blank=True)
    finished_at = models.DateTimeField(null=True, blank=True)
    duration_ms = models.PositiveIntegerField(null=True, blank=True)
    input_tokens = models.PositiveIntegerField(null=True, blank=True)
    output_tokens = models.PositiveIntegerField(null=True, blank=True)
    estimated_cost = models.DecimalField(
        max_digits=14, decimal_places=8, null=True, blank=True)
    retry_count = models.PositiveSmallIntegerField(default=0)
    fallback_count = models.PositiveSmallIntegerField(default=0)
    attempt_number = models.PositiveSmallIntegerField(default=1)
    external_request_id = models.CharField(max_length=255, blank=True, default="")
    idempotency_key = models.CharField(max_length=255, blank=True, default="")
    genuine_result = models.BooleanField(default=False)
    error_code = models.CharField(max_length=80, blank=True, default="")
    error_message = models.TextField(blank=True, default="")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["provider", "status"]),
            models.Index(fields=["user", "idempotency_key"]),
            models.Index(fields=["external_request_id"]),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=["user", "idempotency_key"],
                condition=~models.Q(idempotency_key=""),
                name="unique_ai_execution_idempotency_key",
            ),
        ]



