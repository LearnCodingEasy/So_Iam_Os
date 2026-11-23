from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class RevenueStream(models.Model):
    """A concrete income stream belonging to a source."""

    STATUS_CHOICES = [('active', 'Active'), ('paused', 'Paused'), ('ended', 'Ended')]
    STATUS_ACTIVE = 'active'
    STATUS_PAUSED = 'paused'
    STATUS_ENDED = 'ended'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='revenue_streams')
    source = models.ForeignKey('revenue.RevenueSource', on_delete=models.CASCADE, related_name='streams')
    name = models.CharField(max_length=160)
    description = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
