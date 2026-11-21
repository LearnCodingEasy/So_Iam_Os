from django.db import models
from codex.models.project_registry import ProjectRegistry


class FileRegistry(models.Model):
    project = models.ForeignKey(
        ProjectRegistry, on_delete=models.CASCADE, related_name="files")
    path = models.CharField(max_length=700)
    kind = models.CharField(max_length=80, blank=True)
    app_label = models.CharField(max_length=100, blank=True)
    sha256 = models.CharField(max_length=64, blank=True)
    size = models.PositiveBigIntegerField(default=0)
    protected = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    scanned_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=["project", "path"], name="codex_file_project_path")]
