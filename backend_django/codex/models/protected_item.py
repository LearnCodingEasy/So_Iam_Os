from django.conf import settings
from django.db import models
from codex.models.project_registry import ProjectRegistry


class ProtectedItem(models.Model):
    ITEM_TYPES = [
        ("file", "File"),
        ("directory", "Directory"),
        ("model", "Django Model"),
        ("api", "API Endpoint"),
        ("feature", "Feature"),
        ("component", "Frontend Component"),
        ("service", "Service"),
    ]
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="protected_items")
    key = models.CharField(max_length=220)
    item_type = models.CharField(
        max_length=30, choices=ITEM_TYPES, default="file")
    path = models.CharField(max_length=700, blank=True)
    target = models.CharField(max_length=700, blank=True)
    reason = models.TextField(blank=True)
    approved = models.BooleanField(default=False)
    frozen = models.BooleanField(default=False)
    rules = models.JSONField(default=dict, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    approved_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
                                    null=True, blank=True, related_name="codex_approved_protected_items")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["project", "key"], name="codex_protected_item_project_key_unique"),
        ]
        ordering = ["item_type", "path", "key"]
