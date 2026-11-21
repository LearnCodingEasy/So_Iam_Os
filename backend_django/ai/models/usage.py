
from django.conf import settings
from django.db import models


class AIUsageRecord(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_usage_records"
    )

    execution = models.OneToOneField(
        "ai.AIExecution",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="usage_record"
    )

    provider = models.CharField(max_length=50)
    model = models.CharField(max_length=255, blank=True, default="")
    agent = models.CharField(max_length=120, blank=True, default="")

    input_tokens = models.PositiveIntegerField(default=0)
    output_tokens = models.PositiveIntegerField(default=0)
    cached_input_tokens = models.PositiveIntegerField(default=0)

    estimated_cost = models.DecimalField(
        max_digits=14,
        decimal_places=8,
        default=0
    )

    actual_cost = models.DecimalField(
        max_digits=14,
        decimal_places=8,
        null=True,
        blank=True
    )

    currency = models.CharField(max_length=8, default="USD")
    pricing_version = models.CharField(
        max_length=64,
        blank=True,
        default=""
    )

    cost_source = models.CharField(
        max_length=32,
        default="estimated"
    )

    is_estimated = models.BooleanField(default=True)

    recorded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        indexes = [
            models.Index(fields=["user", "-recorded_at"]),
            models.Index(fields=["provider", "model"]),
        ]

    def __str__(self):
        return f"{self.provider} - {self.model} - User {self.user_id}"





