from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexAgentDefinition(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name='agent_definitions')
    key = models.CharField(max_length=180)
    name = models.CharField(max_length=220)
    category = models.CharField(max_length=120)
    purpose = models.TextField(blank=True)
    input_schema = models.JSONField(default=dict, blank=True)
    output_schema = models.JSONField(default=dict, blank=True)
    tools = models.JSONField(default=list, blank=True)
    permissions = models.JSONField(default=list, blank=True)
    risk = models.CharField(max_length=30, default='medium')
    validation = models.JSONField(default=list, blank=True)
    implementation = models.CharField(
        max_length=120, default='catalog_orchestrator')
    enabled = models.BooleanField(default=True)
    version = models.CharField(max_length=30, default='1.0.0')
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['project', 'key'], name='codex_agent_definition_project_key_unique')]
        ordering = ['category', 'id']
