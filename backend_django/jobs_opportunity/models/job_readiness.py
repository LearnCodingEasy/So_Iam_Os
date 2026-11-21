from django.conf import settings
from django.db import models
from jobs_opportunity.models.common import PERCENT
from jobs_opportunity.models.job_opportunity import JobOpportunity


class JobReadiness(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_readiness")
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="readiness_records")
    score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    level = models.CharField(max_length=30, default="not_ready")
    breakdown = models.JSONField(default=dict, blank=True)
    next_actions = models.JSONField(default=list, blank=True)
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_readiness_unique")]
