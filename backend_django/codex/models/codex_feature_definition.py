from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexFeatureDefinition(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='feature_definitions')
    key = models.CharField(max_length=180)
    name = models.CharField(max_length=220)
    category = models.CharField(max_length=120)
    purpose = models.TextField(blank=True)
    status = models.CharField(max_length=30, default='implemented')
    protection_level = models.CharField(max_length=30, default='NORMAL')
    permissions = models.JSONField(default=list, blank=True)
    integration = models.JSONField(default=dict, blank=True)
    tests = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    enabled = models.BooleanField(default=True)
    version = models.CharField(max_length=30, default='1.0.0')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['project', 'key'], name='codex_feature_definition_project_key_unique')]
        ordering = ['category', 'id']
