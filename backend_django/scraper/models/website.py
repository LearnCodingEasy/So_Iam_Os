import uuid
from django.db import models
from django.conf import settings
from django.utils.timesince import timesince


class Website(models.Model):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    name = models.CharField(max_length=200)
    base_url = models.URLField()
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    SOURCE_TYPES = [
        ("json", "JSON / REST API"),
        ("rss", "RSS / Atom"),
        ("html", "Public HTML"),
    ]
    source_type = models.CharField(max_length=12, choices=SOURCE_TYPES, default="html")
    config = models.JSONField(default=dict, blank=True, help_text="Connector settings; never store secrets here.")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL, related_name="scraper_websites")
    last_run_at = models.DateTimeField(null=True, blank=True)
    last_status = models.CharField(max_length=20, blank=True)
    last_error = models.TextField(blank=True)
    request_timeout = models.PositiveSmallIntegerField(default=15)

    class Meta:
        verbose_name = "Website"
        verbose_name_plural = "Websites"
        ordering = ['-created_at']

    def created_at_formatted(self):
        return timesince(self.created_at)

    def __str__(self):
        return self.name
