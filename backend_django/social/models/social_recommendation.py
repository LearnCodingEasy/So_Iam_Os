from django.db import models
from social.models.common import User


class SocialRecommendation(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_recommendations")
    candidate = models.ForeignKey(User, on_delete=models.CASCADE, related_name="social_recommended_to")
    score = models.PositiveSmallIntegerField(default=0)
    reasons = models.JSONField(default=list, blank=True)
    breakdown = models.JSONField(default=dict, blank=True)
    status = models.CharField(max_length=20, default="active")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "candidate"], name="unique_social_recommendation")]
        indexes = [models.Index(fields=["user", "score"])]
