from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Campaign(models.Model):
    """A time-boxed marketing effort with a budget."""

    STATUS_CHOICES = [('draft', 'Draft'), ('scheduled', 'Scheduled'), ('running', 'Running'), ('completed', 'Completed'), ('cancelled', 'Cancelled')]
    STATUS_DRAFT = 'draft'
    STATUS_SCHEDULED = 'scheduled'
    STATUS_RUNNING = 'running'
    STATUS_COMPLETED = 'completed'
    STATUS_CANCELLED = 'cancelled'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketing_campaigns')
    channel = models.ForeignKey('marketing.MarketingChannel', null=True, blank=True, on_delete=models.SET_NULL, related_name='campaigns')
    name = models.CharField(max_length=200)
    objective = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')
    budget = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    spent = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return str(self.name)
