from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class RevenueSource(models.Model):
    """Where money comes from (a service line, a product, an affiliate programme, ...)."""

    TYPE_CHOICES = [('service', 'Service'), ('product', 'Product'), ('subscription', 'Subscription'), ('affiliate', 'Affiliate'), ('other', 'Other')]
    TYPE_SERVICE = 'service'
    TYPE_PRODUCT = 'product'
    TYPE_SUBSCRIPTION = 'subscription'
    TYPE_AFFILIATE = 'affiliate'
    TYPE_OTHER = 'other'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='revenue_sources')
    name = models.CharField(max_length=160)
    source_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='service')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
