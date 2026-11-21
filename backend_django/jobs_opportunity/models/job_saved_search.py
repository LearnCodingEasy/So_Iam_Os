from django.conf import settings
from django.db import models


class JobSavedSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_saved_searches")
    name = models.CharField(max_length=150)
    query = models.CharField(max_length=255, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    alert_enabled = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
