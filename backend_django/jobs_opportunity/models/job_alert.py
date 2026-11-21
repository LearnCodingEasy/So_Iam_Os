from django.conf import settings
from django.db import models


class JobAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_alerts")
    alert_type = models.CharField(max_length=50, default="job_match")
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read"])]
