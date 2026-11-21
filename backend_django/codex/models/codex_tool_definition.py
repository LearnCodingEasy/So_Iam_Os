from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexToolDefinition(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='tool_definitions')
    key = models.CharField(max_length=180)
    name = models.CharField(max_length=220)
    category = models.CharField(max_length=120)
    capability = models.CharField(max_length=40, default='read')
    risk = models.CharField(max_length=30, default='low')
    permission = models.CharField(max_length=80, default='READ_FILES')
    input_schema = models.JSONField(default=dict, blank=True)
    output_schema = models.JSONField(default=dict, blank=True)
    purpose = models.TextField(blank=True)
    implementation = models.CharField(
        max_length=120, default='catalog_dispatch')
    enabled = models.BooleanField(default=True)
    version = models.CharField(max_length=30, default='1.0.0')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['project', 'key'], name='codex_tool_definition_project_key_unique')]
        ordering = ['category', 'id']
