from django.conf import settings
from django.db import models
from django.utils import timezone
from jobs_opportunity.models.common import PERCENT
from jobs_opportunity.models.company_profile import CompanyProfile
from jobs_opportunity.models.job_source import JobSource


class JobOpportunity(models.Model):
    class JobType(models.TextChoices):
        FULL_TIME = "full_time", "Full time"
        PART_TIME = "part_time", "Part time"
        CONTRACT = "contract", "Contract"
        FREELANCE = "freelance", "Freelance"
        INTERNSHIP = "internship", "Internship"
        PROJECT = "project", "Project"
        TEMPORARY = "temporary", "Temporary"
        VOLUNTEER = "volunteer", "Volunteer"

    class LocationType(models.TextChoices):
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        ONSITE = "onsite", "On-site"
        UNKNOWN = "unknown", "Unknown"

    class ExperienceLevel(models.TextChoices):
        ENTRY = "entry", "Entry"
        JUNIOR = "junior", "Junior"
        MID = "mid", "Mid"
        SENIOR = "senior", "Senior"
        LEAD = "lead", "Lead"
        EXECUTIVE = "executive", "Executive"
        UNKNOWN = "unknown", "Unknown"

    class SalaryPeriod(models.TextChoices):
        HOUR = "hour", "Hourly"
        MONTH = "month", "Monthly"
        YEAR = "year", "Yearly"
        UNKNOWN = "unknown", "Unknown"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_opportunities")
    source = models.ForeignKey(JobSource, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs")
    company_profile = models.ForeignKey(CompanyProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name="jobs")
    external_id = models.CharField(max_length=255, blank=True)
    canonical_key = models.CharField(max_length=400, blank=True, db_index=True)
    title = models.CharField(max_length=255)
    normalized_title = models.CharField(max_length=255, blank=True)
    company = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    responsibilities = models.JSONField(default=list, blank=True)
    benefits = models.JSONField(default=list, blank=True)
    extracted_requirements = models.JSONField(default=list, blank=True)
    url = models.URLField(blank=True, max_length=500)
    location = models.CharField(max_length=255, blank=True)
    location_type = models.CharField(max_length=20, choices=LocationType.choices, default=LocationType.UNKNOWN)
    is_remote = models.BooleanField(default=False)
    job_type = models.CharField(max_length=30, choices=JobType.choices, default=JobType.FULL_TIME)
    experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.UNKNOWN)
    salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    salary_estimated = models.BooleanField(default=False)
    salary_period = models.CharField(max_length=20, choices=SalaryPeriod.choices, default=SalaryPeriod.UNKNOWN)
    currency = models.CharField(max_length=10, default="USD")
    tags = models.JSONField(default=list, blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    ai_summary = models.TextField(blank=True)
    red_flags = models.JSONField(default=list, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)
    application_deadline = models.DateTimeField(null=True, blank=True)
    expires_at = models.DateTimeField(null=True, blank=True)
    discovered_at = models.DateTimeField(default=timezone.now)
    last_checked_at = models.DateTimeField(null=True, blank=True)
    freshness_score = models.PositiveSmallIntegerField(default=50, validators=PERCENT)
    is_active = models.BooleanField(default=True)
    is_expired = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    required_skills = models.ManyToManyField("learning.Skill", through="JobSkillRequirement", related_name="job_opportunities")

    class Meta:
        ordering = ["-published_at", "-discovered_at"]
        indexes = [
            models.Index(fields=["user", "is_active"]),
            models.Index(fields=["user", "is_remote"]),
            models.Index(fields=["source", "external_id"]),
            models.Index(fields=["user", "company"]),
            models.Index(fields=["user", "location_type"]),
            models.Index(fields=["user", "experience_level"]),
            models.Index(fields=["user", "published_at"]),
        ]
        constraints = [
            models.UniqueConstraint(fields=["user", "source", "external_id"], name="jobs_unique_external_per_user_source"),
        ]

    def save(self, *args, **kwargs):
        self.normalized_title = " ".join(self.title.lower().split())
        if not self.location_type or self.location_type == self.LocationType.UNKNOWN:
            if self.is_remote:
                self.location_type = self.LocationType.REMOTE
        if self.expires_at and self.expires_at < timezone.now():
            self.is_expired = True
            self.is_active = False
        super().save(*args, **kwargs)
