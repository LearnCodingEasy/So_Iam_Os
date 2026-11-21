from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexAgentRun(models.Model):
    STATUS = [('planned', 'Planned'), ('approved', 'Approved'), ('running', 'Running'),
              ('completed', 'Completed'), ('failed', 'Failed'), ('cancelled', 'Cancelled')]
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='agent_runs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    request = models.TextField()
    mode = models.CharField(max_length=60, default='safe-agent')
    status = models.CharField(max_length=30, choices=STATUS, default='planned')
    plan = models.JSONField(default=dict, blank=True)
    result = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
