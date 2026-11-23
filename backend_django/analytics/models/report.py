from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Report(models.Model):
    """A saved report definition and its last generated content."""

    TYPE_CHOICES = [('summary', 'Metric summary'), ('metric_trend', 'Metric trend'), ('events', 'Event counts')]
    TYPE_SUMMARY = 'summary'
    TYPE_METRIC_TREND = 'metric_trend'
    TYPE_EVENTS = 'events'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='analytics_reports')
    title = models.CharField(max_length=200)
    report_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='summary')
    period_start = models.DateField(null=True, blank=True)
    period_end = models.DateField(null=True, blank=True)
    parameters = models.JSONField(default=dict, blank=True)
    content = models.JSONField(default=dict, blank=True)
    generated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.title)
