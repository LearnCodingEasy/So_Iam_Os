from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Metric(models.Model):
    """A named measurement the user tracks over time."""

    KIND_CHOICES = [('gauge', 'Gauge'), ('counter', 'Counter')]
    KIND_GAUGE = 'gauge'
    KIND_COUNTER = 'counter'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='metrics')
    key = models.SlugField(max_length=80)
    name = models.CharField(max_length=160)
    unit = models.CharField(max_length=40, blank=True)
    source_app = models.CharField(max_length=60, blank=True)
    description = models.TextField(blank=True)
    kind = models.CharField(max_length=20, choices=KIND_CHOICES, default='gauge')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']
        constraints = [
            models.UniqueConstraint(fields=['user', 'key'], name='analytics_metric_user_key_unique'),
        ]

    def __str__(self):
        return str(self.key)
