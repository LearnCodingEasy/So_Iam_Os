from django.db import models


class ProjectRegistry(models.Model):
    key = models.CharField(max_length=120, unique=True, default="so_iam_os")
    name = models.CharField(max_length=200, default="SO_IAM_OS")
    root_path = models.CharField(max_length=500, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    scanned_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
