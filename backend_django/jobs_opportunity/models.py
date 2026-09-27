from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


class JobSource(models.Model):
    class SourceType(models.TextChoices):
        API = "api", "Official API"
        RSS = "rss", "RSS/Public Feed"
        MANUAL = "manual", "Manual"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_sources")
    name = models.CharField(max_length=150)
    source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.MANUAL)
    base_url = models.URLField(blank=True)
    feed_url = models.URLField(blank=True)
    enabled = models.BooleanField(default=True)
    config = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    last_sync_status = models.CharField(max_length=20, default="never")
    last_sync_error = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["user", "name"], name="jobs_source_user_name_unique")]


class JobOpportunity(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = "full_time", "Full time"
        PART_TIME = "part_time", "Part time"
        CONTRACT = "contract", "Contract"
        FREELANCE = "freelance", "Freelance"
        INTERNSHIP = "internship", "Internship"
        PROJECT = "project", "Project"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_opportunities")
    source = models.ForeignKey(JobSource, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs")
    external_id = models.CharField(max_length=255, blank=True)
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    url = models.URLField(blank=True)
    location = models.CharField(max_length=255, blank=True)
    is_remote = models.BooleanField(default=False)
    job_type = models.CharField(max_length=30, choices=JobType.choices, default=JobType.FULL_TIME)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="USD")
    required_skills = models.ManyToManyField("learning.Skill", through="JobSkillRequirement", related_name="job_opportunities")
    metadata = models.JSONField(default=dict, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    discovered_at = models.DateTimeField(default=timezone.now)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-published_at", "-discovered_at"]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["user", "is_remote"]),
            models.Index(fields=["source", "external_id"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["user", "source", "external_id"], name="jobs_unique_external_per_user_source"),
        ]


class JobSkillRequirement(models.Model):
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="skill_requirements")
    skill = models.ForeignKey("learning.Skill", on_delete=models.CASCADE, related_name="job_requirements")
    required_level = models.CharField(max_length=20, choices=[(x.value, x.label) for x in __import__("learning.models", fromlist=["Skill"]).Skill.Level], default="intermediate")
    importance = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

    class Meta:
        constraints = [models.UniqueConstraint(fields=["job", "skill"], name="jobs_job_skill_unique")]


class JobMatch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_matches")
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="matches")
    score = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    matched_skills = models.JSONField(default=list, blank=True)
    missing_skills = models.JSONField(default=list, blank=True)
    reasons = models.JSONField(default=list, blank=True)
    calculated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-score", "-calculated_at"]
        constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_match_unique")]


class JobApplication(models.Model):
    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        APPLIED = "applied", "Applied"
        INTERVIEW = "interview", "Interview"
        OFFER = "offer", "Offer"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_applications")
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="applications")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SAVED)
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_application_unique")]
