from django.db import models
from codex.models.project_registry import ProjectRegistry


class Feature(models.Model):
    STATUS_CHOICES = [("active", "Active"), ("planned",
                                             "Planned"), ("deprecated", "Deprecated")]
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="features")
    key = models.CharField(max_length=180)
    name = models.CharField(max_length=220)
    app_label = models.CharField(max_length=100, blank=True)
    description = models.TextField(blank=True)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="active")
    protected = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["project", "key"], name="codex_feature_project_key")]
