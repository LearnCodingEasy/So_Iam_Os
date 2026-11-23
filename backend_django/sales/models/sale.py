from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Sale(models.Model):
    """A completed transaction. Source record for revenue attribution."""

    STATUS_CHOICES = [('completed', 'Completed'), ('refunded', 'Refunded')]
    STATUS_COMPLETED = 'completed'
    STATUS_REFUNDED = 'refunded'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales_records')
    deal = models.ForeignKey('sales.Deal', null=True, blank=True, on_delete=models.SET_NULL, related_name='sales')
    offer = models.ForeignKey('sales.Offer', null=True, blank=True, on_delete=models.SET_NULL, related_name='sales')
    contact = models.ForeignKey('crm.Contact', null=True, blank=True, on_delete=models.SET_NULL, related_name='sales')
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    sold_at = models.DateTimeField(default=timezone.now)
    reference = models.CharField(max_length=120, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-sold_at']

    def __str__(self):
        return str('%s %s' % (self.amount, self.currency))
