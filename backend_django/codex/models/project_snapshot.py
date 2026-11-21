from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class ProjectSnapshot(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="snapshots")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    label = models.CharField(max_length=220)
    manifest = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
