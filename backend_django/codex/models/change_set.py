from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class ChangeSet(models.Model):
    STATUS = [("planned", "Planned"), ("approved", "Approved"), ("applied",
                                                                 "Applied"), ("rolled_back", "Rolled back"), ("rejected", "Rejected")]
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="changesets")
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, blank=True)
    title = models.CharField(max_length=240)
    objective = models.TextField(blank=True)
    status = models.CharField(max_length=30, choices=STATUS, default="planned")
    impact = models.JSONField(default=dict, blank=True)
    plan = models.JSONField(default=list, blank=True)
    diff_summary = models.JSONField(default=dict, blank=True)
    snapshot_id = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
