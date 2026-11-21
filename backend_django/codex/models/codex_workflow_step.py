from django.db import models
from codex.models.project_registry import ProjectRegistry


class CodexWorkflowStep(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("in_progress", "In Progress"),
        ("completed", "Completed"),
        ("blocked", "Blocked"),
        ("skipped", "Skipped"),
    ]
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="workflow_steps")
    key = models.CharField(max_length=120)
    name = models.CharField(max_length=220)
    order = models.PositiveIntegerField(default=0)
    status = models.CharField(
        max_length=30, choices=STATUS_CHOICES, default="pending")
    description = models.TextField(blank=True)
    dependencies = models.JSONField(default=list, blank=True)
    checks = models.JSONField(default=list, blank=True)
    evidence = models.JSONField(default=dict, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "key"], name="codex_workflow_step_project_key_unique"),
        ]
        ordering = ["order", "id"]
