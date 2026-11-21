from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexAuditEvent(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='audit_events')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    event_type = models.CharField(max_length=100)
    action = models.CharField(max_length=180)
    status = models.CharField(max_length=40, default='success')
    payload = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
