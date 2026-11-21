from django.conf import settings
from django.db import models
from jobs_opportunity.models.job_opportunity import JobOpportunity


class JobSkillGap(models.Model):
    class Severity(models.TextChoices):
        LOW = "low", "Low"
        MEDIUM = "medium", "Medium"
        HIGH = "high", "High"
        CRITICAL = "critical", "Critical"

    class Status(models.TextChoices):
        OPEN = "open", "Open"
        LEARNING = "learning", "Learning"
        READY = "ready", "Ready"
        DISMISSED = "dismissed", "Dismissed"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_skill_gaps")
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="skill_gaps")
    skill = models.ForeignKey("learning.Skill", on_delete=models.SET_NULL, null=True, blank=True, related_name="job_skill_gaps")
    name = models.CharField(max_length=150)
    required_level = models.CharField(max_length=20, default="intermediate")
    current_level = models.CharField(max_length=20, blank=True)
    severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MEDIUM)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)
    learning_goal = models.ForeignKey("learning.LearningGoal", on_delete=models.SET_NULL, null=True, blank=True, related_name="job_skill_gaps")
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "job", "name"], name="jobs_user_job_gap_name_unique")]
        indexes = [models.Index(fields=["user", "status"]), models.Index(fields=["job", "severity"])]
