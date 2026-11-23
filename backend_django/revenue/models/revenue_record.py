from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class RevenueRecord(models.Model):
    """Money actually received. May reference the originating sale for attribution."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='revenue_records')
    stream = models.ForeignKey('revenue.RevenueStream', null=True, blank=True, on_delete=models.SET_NULL, related_name='records')
    sale = models.ForeignKey('sales.Sale', null=True, blank=True, on_delete=models.SET_NULL, related_name='revenue_records')
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    received_on = models.DateField()
    description = models.CharField(max_length=255, blank=True)
    reference = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-received_on', '-id']
        constraints = [
            models.UniqueConstraint(fields=['sale'], name='revenue_record_sale_unique'),
        ]

    def __str__(self):
        return str('%s %s' % (self.amount, self.currency))
