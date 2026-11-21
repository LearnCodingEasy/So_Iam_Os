from django.db import models
from social.models.common import User


class SocialProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="social_profile")
    learning_interests = models.JSONField(default=list, blank=True)
    professional_interests = models.JSONField(default=list, blank=True)
    topics = models.JSONField(default=list, blank=True)
    looking_for = models.JSONField(default=list, blank=True)
    bio = models.TextField(blank=True)
    discoverable = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [models.Index(fields=["discoverable", "updated_at"])]
