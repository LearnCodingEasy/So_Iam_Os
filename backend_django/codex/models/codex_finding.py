from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexFinding(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='findings')
    category = models.CharField(max_length=80)
    severity = models.CharField(max_length=30, default='medium')
    title = models.CharField(max_length=220)
    path = models.CharField(max_length=700, blank=True)
    line = models.PositiveIntegerField(null=True, blank=True)
    message = models.TextField()
    metadata = models.JSONField(default=dict, blank=True)
    resolved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
