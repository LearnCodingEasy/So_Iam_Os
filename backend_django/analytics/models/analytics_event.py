from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class AnalyticsEvent(models.Model):
    """A discrete occurrence worth counting (e.g. a lesson finished, an offer sent)."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analytics_events')
    name = models.CharField(max_length=120)
    source_app = models.CharField(max_length=60, blank=True)
    properties = models.JSONField(default=dict, blank=True)
    occurred_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-occurred_at']

    def __str__(self):
        return str(self.name)
