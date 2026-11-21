from django.conf import settings
from django.db import models
from jobs_opportunity.models.common import PERCENT
from jobs_opportunity.models.job_opportunity import JobOpportunity


class JobRecommendation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_recommendations")
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="recommendations")
    score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    reasons = models.JSONField(default=list, blank=True)
    is_seen = models.BooleanField(default=False)
    is_saved = models.BooleanField(default=False)
    is_dismissed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_recommendation_unique")]
        ordering = ["-score", "-updated_at"]
