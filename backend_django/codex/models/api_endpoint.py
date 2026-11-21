from django.db import models
from codex.models.project_registry import ProjectRegistry


class APIEndpoint(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="apis")
    method = models.CharField(max_length=16, default="ANY")
    path = models.CharField(max_length=700)
    name = models.CharField(max_length=240, blank=True)
    source = models.CharField(max_length=300, blank=True)
    app_label = models.CharField(max_length=100, blank=True)
    frontend_route = models.CharField(max_length=220, default="/codex")
    frontend_section = models.CharField(max_length=160, default="API Registry")
    frontend_service = models.CharField(max_length=220, blank=True)
    coverage_status = models.CharField(
        max_length=40, default="registry-covered")
    protected = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["project", "method", "path", "name"], name="codex_api_unique")]
