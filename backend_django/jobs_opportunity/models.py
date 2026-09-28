from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone


PERCENT = [MinValueValidator(0), MaxValueValidator(100)]


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
    sync_interval_minutes = models.PositiveIntegerField(default=60)
    max_items_per_sync = models.PositiveIntegerField(default=100)
    config = models.JSONField(default=dict, blank=True)
    last_synced_at = models.DateTimeField(null=True, blank=True)
    last_sync_status = models.CharField(max_length=20, default="never")
    last_sync_error = models.TextField(blank=True)
    last_sync_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["user", "name"], name="jobs_source_user_name_unique")]


class CompanyProfile(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_companies")
    name = models.CharField(max_length=255)
    normalized_name = models.CharField(max_length=255, blank=True)
    website = models.URLField(blank=True)
    industry = models.CharField(max_length=150, blank=True)
    location = models.CharField(max_length=255, blank=True)
    size = models.CharField(max_length=80, blank=True)
    description = models.TextField(blank=True)
    is_followed = models.BooleanField(default=False)
    is_blacklisted = models.BooleanField(default=False)
    notes = models.TextField(blank=True)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["name"]
        constraints = [models.UniqueConstraint(fields=["user", "normalized_name"], name="jobs_company_user_normalized_unique")]

    def save(self, *args, **kwargs):
        if not self.normalized_name:
            self.normalized_name = " ".join(self.name.lower().split())
        super().save(*args, **kwargs)


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
    url = models.URLField(blank=True)
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


class JobSkillRequirement(models.Model):
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="skill_requirements")
    skill = models.ForeignKey("learning.Skill", on_delete=models.CASCADE, related_name="job_requirements")
    required_level = models.CharField(max_length=20, choices=[(x.value, x.label) for x in __import__("learning.models", fromlist=["Skill"]).Skill.Level], default="intermediate")
    importance = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])
    requirement_type = models.CharField(max_length=20, choices=[("required", "Required"), ("preferred", "Preferred"), ("optional", "Optional")], default="required")

    class Meta:
        constraints = [models.UniqueConstraint(fields=["job", "skill"], name="jobs_job_skill_unique")]


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


class JobApplication(models.Model):
    class Status(models.TextChoices):
        SAVED = "saved", "Saved"
        PREPARING = "preparing", "Preparing"
        APPLIED = "applied", "Applied"
        SCREENING = "screening", "Screening"
        INTERVIEW = "interview", "Interview"
        TECHNICAL = "technical", "Technical Interview"
        FINAL = "final", "Final Interview"
        OFFER = "offer", "Offer"
        ACCEPTED = "accepted", "Accepted"
        REJECTED = "rejected", "Rejected"
        WITHDRAWN = "withdrawn", "Withdrawn"

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_applications")
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="applications")
    resume = models.ForeignKey("JobResume", on_delete=models.SET_NULL, null=True, blank=True, related_name="applications")
    cover_letter = models.ForeignKey("JobCoverLetter", on_delete=models.SET_NULL, null=True, blank=True, related_name="applications")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.SAVED)
    notes = models.TextField(blank=True)
    applied_at = models.DateTimeField(null=True, blank=True)
    deadline = models.DateTimeField(null=True, blank=True)
    expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    offer_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    offer_currency = models.CharField(max_length=10, blank=True)
    rejection_reason = models.CharField(max_length=255, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_application_unique")]
        indexes = [models.Index(fields=["user", "status"]), models.Index(fields=["user", "deadline"])]


class JobApplicationEvent(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    note = models.TextField(blank=True)
    occurred_at = models.DateTimeField(default=timezone.now)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-occurred_at"]
        indexes = [models.Index(fields=["application", "occurred_at"])]


class JobInterview(models.Model):
    application = models.ForeignKey(JobApplication, on_delete=models.CASCADE, related_name="interviews")
    stage = models.CharField(max_length=80, default="Interview")
    scheduled_at = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.PositiveIntegerField(default=60)
    location = models.CharField(max_length=255, blank=True)
    notes = models.TextField(blank=True)
    questions = models.JSONField(default=list, blank=True)
    feedback = models.TextField(blank=True)
    rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class JobResume(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_resumes")
    title = models.CharField(max_length=150)
    file = models.FileField(upload_to="jobs/resumes/%Y/%m/", blank=True)
    content = models.TextField(blank=True)
    is_default = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-is_default", "-updated_at"]


class JobCoverLetter(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_cover_letters")
    job = models.ForeignKey(JobOpportunity, on_delete=models.CASCADE, related_name="cover_letters")
    resume = models.ForeignKey(JobResume, on_delete=models.SET_NULL, null=True, blank=True, related_name="cover_letters")
    title = models.CharField(max_length=150, default="Cover Letter")
    content = models.TextField()
    version = models.PositiveIntegerField(default=1)
    generated = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class JobPreference(models.Model):
    class RemotePreference(models.TextChoices):
        ANY = "any", "Any"
        REMOTE = "remote", "Remote"
        HYBRID = "hybrid", "Hybrid"
        ONSITE = "onsite", "On-site"

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_preference")
    target_titles = models.JSONField(default=list, blank=True)
    locations = models.JSONField(default=list, blank=True)
    preferred_job_types = models.JSONField(default=list, blank=True)
    preferred_skills = models.JSONField(default=list, blank=True)
    excluded_companies = models.JSONField(default=list, blank=True)
    preferred_companies = models.JSONField(default=list, blank=True)
    remote_preference = models.CharField(max_length=20, choices=RemotePreference.choices, default=RemotePreference.ANY)
    min_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    max_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=10, default="USD")
    score_weights = models.JSONField(default=dict, blank=True)
    notification_settings = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class JobSavedSearch(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_saved_searches")
    name = models.CharField(max_length=150)
    query = models.CharField(max_length=255, blank=True)
    filters = models.JSONField(default=dict, blank=True)
    alert_enabled = models.BooleanField(default=True)
    last_run_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


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


class JobAlert(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_alerts")
    alert_type = models.CharField(max_length=50, default="job_match")
    title = models.CharField(max_length=255)
    message = models.TextField(blank=True)
    url = models.CharField(max_length=500, blank=True)
    is_read = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["user", "is_read"])]


class JobAnalyticsSnapshot(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_analytics_snapshots")
    snapshot_date = models.DateField(default=timezone.localdate)
    metrics = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "snapshot_date"], name="jobs_user_snapshot_date_unique")]
