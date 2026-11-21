from django.conf import settings
from django.db import models
from django.utils import timezone


class JobAnalyticsSnapshot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_analytics_snapshots")
    snapshot_date = models.DateField(default=timezone.localdate)
    metrics = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "snapshot_date"], name="jobs_user_snapshot_date_unique")]
