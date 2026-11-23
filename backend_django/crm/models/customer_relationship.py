from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class CustomerRelationship(models.Model):
    """The commercial relationship stage of a contact (one per contact)."""

    STAGE_CHOICES = [('lead', 'Lead'), ('prospect', 'Prospect'), ('customer', 'Customer'), ('partner', 'Partner'), ('churned', 'Churned')]
    STAGE_LEAD = 'lead'
    STAGE_PROSPECT = 'prospect'
    STAGE_CUSTOMER = 'customer'
    STAGE_PARTNER = 'partner'
    STAGE_CHURNED = 'churned'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crm_relationships')
    contact = models.OneToOneField('crm.Contact', on_delete=models.CASCADE, related_name='relationship')
    stage = models.CharField(max_length=20, choices=STAGE_CHOICES, default='lead')
    health_score = models.PositiveSmallIntegerField(default=50)
    next_step = models.TextField(blank=True)
    stage_changed_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return str('%s:%s' % (self.contact_id, self.stage))
