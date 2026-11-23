from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class RecurringRevenue(models.Model):
    """A repeating charge (subscription/retainer) used to compute MRR."""

    INTERVAL_CHOICES = [('monthly', 'Monthly'), ('quarterly', 'Quarterly'), ('yearly', 'Yearly')]
    STATUS_CHOICES = [('active', 'Active'), ('paused', 'Paused'), ('cancelled', 'Cancelled')]
    INTERVAL_MONTHLY = 'monthly'
    INTERVAL_QUARTERLY = 'quarterly'
    INTERVAL_YEARLY = 'yearly'
    STATUS_ACTIVE = 'active'
    STATUS_PAUSED = 'paused'
    STATUS_CANCELLED = 'cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='recurring_revenue')
    stream = models.ForeignKey('revenue.RevenueStream', on_delete=models.CASCADE, related_name='recurring_items')
    name = models.CharField(max_length=160, blank=True)
    amount = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    interval = models.CharField(max_length=20, choices=INTERVAL_CHOICES, default='monthly')
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-start_date', '-id']

    def __str__(self):
        return str('%s %s/%s' % (self.amount, self.currency, self.interval))
