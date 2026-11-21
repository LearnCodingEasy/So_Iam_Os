from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexTool(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='tools')
    key = models.CharField(max_length=160)
    name = models.CharField(max_length=220)
    capability = models.CharField(max_length=60, default='read')
    enabled = models.BooleanField(default=True)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['project', 'key'], name='codex_tool_project_key_unique')]
