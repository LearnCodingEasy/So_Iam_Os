from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class Interaction(models.Model):
    """A logged touchpoint with a contact."""

    TYPE_CHOICES = [('call', 'Call'), ('email', 'Email'), ('meeting', 'Meeting'), ('message', 'Message'), ('note', 'Note')]
    TYPE_CALL = 'call'
    TYPE_EMAIL = 'email'
    TYPE_MEETING = 'meeting'
    TYPE_MESSAGE = 'message'
    TYPE_NOTE = 'note'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='crm_interactions')
    contact = models.ForeignKey('crm.Contact', on_delete=models.CASCADE, related_name='interactions')
    interaction_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='note')
    subject = models.CharField(max_length=200)
    notes = models.TextField(blank=True)
    occurred_at = models.DateTimeField(default=timezone.now)
    follow_up_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-occurred_at']

    def __str__(self):
        return str(self.subject)
