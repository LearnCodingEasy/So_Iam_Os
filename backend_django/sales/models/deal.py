from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Deal(models.Model):
    """A sales opportunity moving through the pipeline. Stage changes go through the service."""

    STAGE_CHOICES = [('prospecting', 'Prospecting'), ('qualified', 'Qualified'), ('proposal', 'Proposal'), ('negotiation', 'Negotiation'), ('won', 'Won'), ('lost', 'Lost')]
    STAGE_PROSPECTING = 'prospecting'
    STAGE_QUALIFIED = 'qualified'
    STAGE_PROPOSAL = 'proposal'
    STAGE_NEGOTIATION = 'negotiation'
    STAGE_WON = 'won'
    STAGE_LOST = 'lost'
    OPEN_STAGES = ('prospecting', 'qualified', 'proposal', 'negotiation')

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales_deals')
    contact = models.ForeignKey('crm.Contact', null=True, blank=True, on_delete=models.SET_NULL, related_name='deals')
    offer = models.ForeignKey('sales.Offer', null=True, blank=True, on_delete=models.SET_NULL, related_name='deals')
    title = models.CharField(max_length=200)
    value = models.DecimalField(max_digits=14, decimal_places=2, default=0)
    currency = models.CharField(max_length=3, default='USD')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='prospecting')
    expected_close_date = models.DateField(null=True, blank=True)
    closed_at = models.DateTimeField(null=True, blank=True)
    lost_reason = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str(self.title)
