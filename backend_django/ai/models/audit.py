from django.conf import settings
from django.db import models


class AiAuditLog(models.Model):
    """Simple event log introduced by migration 0014."""

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="ai_audit_logs",
    )
    action = models.CharField(max_length=255)
    resource = models.CharField(max_length=255, blank=True, null=True)
    details = models.JSONField(default=dict, blank=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["user", "created_at"]),
            models.Index(fields=["action"]),
        ]

    def __str__(self):
        return f"[{self.created_at}] {self.user}: {self.action}"
