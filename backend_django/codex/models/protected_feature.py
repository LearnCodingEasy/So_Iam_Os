from django.db import models
from codex.models.feature import Feature
from codex.models.project_registry import ProjectRegistry


class ProtectedFeature(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="protected_features")
    feature = models.ForeignKey(Feature, on_delete=models.CASCADE,
                                related_name="protection_rules", null=True, blank=True)
    key = models.CharField(max_length=180)
    reason = models.TextField(blank=True)
    paths = models.JSONField(default=list, blank=True)
    rules = models.JSONField(default=dict, blank=True)
    enabled = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["project", "key"], name="codex_protected_project_key")]
