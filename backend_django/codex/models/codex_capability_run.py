from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexCapabilityRun(models.Model):
    KIND_CHOICES = [('tool', 'Tool'), ('agent', 'Agent'),
                    ('feature', 'Feature')]
    STATUS_CHOICES = [('planned', 'Planned'), ('completed',
                                               'Completed'), ('failed', 'Failed'), ('denied', 'Denied')]
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='capability_runs')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.SET_NULL, null=True, blank=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES)
    key = models.CharField(max_length=180)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default='planned')
    input_data = models.JSONField(default=dict, blank=True)
    output_data = models.JSONField(default=dict, blank=True)
    validation = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    completed_at = models.DateTimeField(null=True, blank=True)
