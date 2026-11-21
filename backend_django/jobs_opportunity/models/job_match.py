from django.conf import settings
from django.db import models
from jobs_opportunity.models.common import PERCENT
from jobs_opportunity.models.job_opportunity import JobOpportunity


class JobMatch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_matches")
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="matches")
    score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    skill_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    experience_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    preference_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    goal_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    salary_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    location_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    reasons = models.JSONField(default=list, blank=True)
    breakdown = models.JSONField(default=dict, blank=True)
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-score", "-calculated_at"]
        constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_match_unique")]
