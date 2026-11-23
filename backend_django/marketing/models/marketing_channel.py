from django.conf import settings  # noqa: F401
from django.db import models
from django.utils import timezone  # noqa: F401


class MarketingChannel(models.Model):
    """A place where the user promotes something."""

    TYPE_CHOICES = [('social', 'Social'), ('email', 'Email'), ('content', 'Content'), ('ads', 'Ads'), ('event', 'Event'), ('referral', 'Referral'), ('other', 'Other')]
    TYPE_SOCIAL = 'social'
    TYPE_EMAIL = 'email'
    TYPE_CONTENT = 'content'
    TYPE_ADS = 'ads'
    TYPE_EVENT = 'event'
    TYPE_REFERRAL = 'referral'
    TYPE_OTHER = 'other'

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='marketing_channels')
    name = models.CharField(max_length=160)
    channel_type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='social')
    url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return str(self.name)
