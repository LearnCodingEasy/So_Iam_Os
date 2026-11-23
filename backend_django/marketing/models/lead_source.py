from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class LeadSource(models.Model):
    """Where leads come from; links to the CRM contacts it produced."""

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketing_lead_sources')
    name = models.CharField(max_length=160)
    channel = models.ForeignKey('marketing.MarketingChannel', null=True, blank=True, on_delete=models.SET_NULL, related_name='lead_sources')
    campaign = models.ForeignKey('marketing.Campaign', null=True, blank=True, on_delete=models.SET_NULL, related_name='lead_sources')
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    contacts = models.ManyToManyField('crm.Contact', blank=True, related_name='lead_sources')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
