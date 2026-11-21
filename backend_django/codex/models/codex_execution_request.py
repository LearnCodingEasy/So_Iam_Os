from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexExecutionRequest(models.Model):
    STATUS = [('pending', 'Pending'), ('approved', 'Approved'), ('running', 'Running'),
              ('completed', 'Completed'), ('failed', 'Failed'), ('denied', 'Denied')]
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='execution_requests')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    tool_key = models.CharField(max_length=160)
    status = models.CharField(max_length=30, choices=STATUS, default='pending')
    approval_note = models.TextField(blank=True)
    result = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
