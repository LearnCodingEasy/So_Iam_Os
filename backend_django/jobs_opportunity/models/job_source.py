from django.conf import settings
from django.db import models


class JobSource(models.Model):
    class SourceType(models.TextChoices):
        API = "api", "Official API"
        RSS = "rss", "RSS/Public Feed"
        MANUAL = "manual", "Manual"
        SCRAPER = "scraper", "HTML Scraper"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_sources")
    name = models.CharField(max_length=150)
    source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.MANUAL)
    base_url = models.URLField(blank=True)
    feed_url = models.URLField(blank=True)
    enabled = models.BooleanField(default=True)
    sync_interval_minutes = models.PositiveIntegerField(default=60)
    max_items_per_sync = models.PositiveIntegerField(default=100)
    config = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    last_sync_status = models.CharField(max_length=20, default="never")
    last_sync_error = models.TextField(blank=True)
    last_sync_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["user", "name"], name="jobs_source_user_name_unique")]
