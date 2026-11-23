from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class MetricSnapshot(models.Model):
    """One recorded value of a metric at a point in time."""

    metric = models.ForeignKey('analytics.Metric', on_delete=models.CASCADE, related_name='snapshots')
    value = models.DecimalField(max_digits=20, decimal_places=4)
    recorded_at = models.DateTimeField(default=timezone.now)
    dimensions = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-recorded_at']

    def __str__(self):
        return str('%s=%s' % (self.metric_id, self.value))
