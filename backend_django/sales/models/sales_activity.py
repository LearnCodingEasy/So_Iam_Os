from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class SalesActivity(models.Model):
    """A logged selling action on a deal (call, demo, proposal sent, ...)."""

    TYPE_CHOICES = [('call', 'Call'), ('email', 'Email'), ('meeting', 'Meeting'), ('demo', 'Demo'), ('proposal', 'Proposal'), ('note', 'Note')]
    TYPE_CALL = 'call'
    TYPE_EMAIL = 'email'
    TYPE_MEETING = 'meeting'
    TYPE_DEMO = 'demo'
    TYPE_PROPOSAL = 'proposal'
    TYPE_NOTE = 'note'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='sales_activities')
    deal = models.ForeignKey('sales.Deal', on_delete=models.CASCADE, related_name='activities')
    activity_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='note')
    notes = models.TextField(blank=True)
    occurred_at = models.DateTimeField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-occurred_at']

    def __str__(self):
        return str('%s:%s' % (self.deal_id, self.activity_type))
