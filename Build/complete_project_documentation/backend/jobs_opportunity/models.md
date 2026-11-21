# jobs_opportunity models

Model files and declarations are extracted from source. Field excerpts retain source line numbers; inspect linked source for multiline options and complete semantics.


## common
Source: jobs_opportunity/models/common.py

## company_profile
Source: jobs_opportunity/models/company_profile.py

- L5: class CompanyProfile(models.Model):

- L7: name = models.CharField(max_length=255)

- L8: normalized_name = models.CharField(max_length=255, blank=True)

- L9: website = models.URLField(blank=True)

- L10: industry = models.CharField(max_length=150, blank=True)

- L11: location = models.CharField(max_length=255, blank=True)

- L12: size = models.CharField(max_length=80, blank=True)

- L13: description = models.TextField(blank=True)

- L14: is_followed = models.BooleanField(default=False)

- L15: is_blacklisted = models.BooleanField(default=False)

- L16: notes = models.TextField(blank=True)

- L17: metadata = models.JSONField(default=dict, blank=True)

- L18: created_at = models.DateTimeField(auto_now_add=True)

- L19: updated_at = models.DateTimeField(auto_now=True)

- L21: class Meta:

- L23: constraints = [models.UniqueConstraint(fields=["user", "normalized_name"], name="jobs_company_user_normalized_unique")]

## job_alert
Source: jobs_opportunity/models/job_alert.py

- L5: class JobAlert(models.Model):

- L7: alert_type = models.CharField(max_length=50, default="job_match")

- L8: title = models.CharField(max_length=255)

- L9: message = models.TextField(blank=True)

- L10: url = models.CharField(max_length=500, blank=True)

- L11: is_read = models.BooleanField(default=False)

- L12: metadata = models.JSONField(default=dict, blank=True)

- L13: created_at = models.DateTimeField(auto_now_add=True)

- L15: class Meta:

- L17: indexes = [models.Index(fields=["user", "is_read"])]

## job_analytics_snapshot
Source: jobs_opportunity/models/job_analytics_snapshot.py

- L6: class JobAnalyticsSnapshot(models.Model):

- L8: snapshot_date = models.DateField(default=timezone.localdate)

- L9: metrics = models.JSONField(default=dict, blank=True)

- L10: created_at = models.DateTimeField(auto_now_add=True)

- L12: class Meta:

- L13: constraints = [models.UniqueConstraint(fields=["user", "snapshot_date"], name="jobs_user_snapshot_date_unique")]

## job_application
Source: jobs_opportunity/models/job_application.py

- L6: class JobApplication(models.Model):

- L7: class Status(models.TextChoices):

- L24: status = models.CharField(max_length=20, choices=Status.choices, default=Status.SAVED)

- L25: notes = models.TextField(blank=True)

- L26: applied_at = models.DateTimeField(null=True, blank=True)

- L27: deadline = models.DateTimeField(null=True, blank=True)

- L28: expected_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

- L29: offer_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

- L30: offer_currency = models.CharField(max_length=10, blank=True)

- L31: rejection_reason = models.CharField(max_length=255, blank=True)

- L32: created_at = models.DateTimeField(auto_now_add=True)

- L33: updated_at = models.DateTimeField(auto_now=True)

- L35: class Meta:

- L36: constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_application_unique")]

- L37: indexes = [models.Index(fields=["user", "status"]), models.Index(fields=["user", "deadline"])]

## job_application_event
Source: jobs_opportunity/models/job_application_event.py

- L6: class JobApplicationEvent(models.Model):

- L8: event_type = models.CharField(max_length=50)

- L9: title = models.CharField(max_length=255)

- L10: note = models.TextField(blank=True)

- L11: occurred_at = models.DateTimeField(default=timezone.now)

- L12: metadata = models.JSONField(default=dict, blank=True)

- L14: class Meta:

- L16: indexes = [models.Index(fields=["application", "occurred_at"])]

## job_cover_letter
Source: jobs_opportunity/models/job_cover_letter.py

- L7: class JobCoverLetter(models.Model):

- L11: title = models.CharField(max_length=150, default="Cover Letter")

- L12: content = models.TextField()

- L13: version = models.PositiveIntegerField(default=1)

- L14: generated = models.BooleanField(default=False)

- L15: created_at = models.DateTimeField(auto_now_add=True)

- L16: updated_at = models.DateTimeField(auto_now=True)

## job_interview
Source: jobs_opportunity/models/job_interview.py

- L6: class JobInterview(models.Model):

- L8: stage = models.CharField(max_length=80, default="Interview")

- L9: scheduled_at = models.DateTimeField(null=True, blank=True)

- L10: duration_minutes = models.PositiveIntegerField(default=60)

- L11: location = models.CharField(max_length=255, blank=True)

- L12: notes = models.TextField(blank=True)

- L13: questions = models.JSONField(default=list, blank=True)

- L14: feedback = models.TextField(blank=True)

- L15: rating = models.PositiveSmallIntegerField(default=0, validators=[MinValueValidator(0), MaxValueValidator(5)])

- L16: completed = models.BooleanField(default=False)

- L17: created_at = models.DateTimeField(auto_now_add=True)

- L18: updated_at = models.DateTimeField(auto_now=True)

## job_match
Source: jobs_opportunity/models/job_match.py

- L7: class JobMatch(models.Model):

- L10: score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L11: skill_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L12: experience_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L13: preference_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L14: goal_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L15: salary_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L16: location_score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L17: matched_skills = models.JSONField(default=list, blank=True)

- L18: missing_skills = models.JSONField(default=list, blank=True)

- L19: reasons = models.JSONField(default=list, blank=True)

- L20: breakdown = models.JSONField(default=dict, blank=True)

- L21: calculated_at = models.DateTimeField(auto_now=True)

- L23: class Meta:

- L25: constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_match_unique")]

## job_opportunity
Source: jobs_opportunity/models/job_opportunity.py

- L9: class JobOpportunity(models.Model):

- L10: class JobType(models.TextChoices):

- L20: class LocationType(models.TextChoices):

- L26: class ExperienceLevel(models.TextChoices):

- L35: class SalaryPeriod(models.TextChoices):

- L44: external_id = models.CharField(max_length=255, blank=True)

- L45: canonical_key = models.CharField(max_length=400, blank=True, db_index=True)

- L46: title = models.CharField(max_length=255)

- L47: normalized_title = models.CharField(max_length=255, blank=True)

- L48: company = models.CharField(max_length=255, blank=True)

- L49: description = models.TextField(blank=True)

- L50: responsibilities = models.JSONField(default=list, blank=True)

- L51: benefits = models.JSONField(default=list, blank=True)

- L52: extracted_requirements = models.JSONField(default=list, blank=True)

- L53: url = models.URLField(blank=True, max_length=500)

- L54: location = models.CharField(max_length=255, blank=True)

- L55: location_type = models.CharField(max_length=20, choices=LocationType.choices, default=LocationType.UNKNOWN)

- L56: is_remote = models.BooleanField(default=False)

- L57: job_type = models.CharField(max_length=30, choices=JobType.choices, default=JobType.FULL_TIME)

- L58: experience_level = models.CharField(max_length=20, choices=ExperienceLevel.choices, default=ExperienceLevel.UNKNOWN)

- L59: salary_min = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

- L60: salary_max = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

- L61: salary_estimated = models.BooleanField(default=False)

- L62: salary_period = models.CharField(max_length=20, choices=SalaryPeriod.choices, default=SalaryPeriod.UNKNOWN)

- L63: currency = models.CharField(max_length=10, default="USD")

- L64: tags = models.JSONField(default=list, blank=True)

- L65: metadata = models.JSONField(default=dict, blank=True)

- L66: ai_summary = models.TextField(blank=True)

- L67: red_flags = models.JSONField(default=list, blank=True)

- L68: published_at = models.DateTimeField(null=True, blank=True)

- L69: application_deadline = models.DateTimeField(null=True, blank=True)

- L70: expires_at = models.DateTimeField(null=True, blank=True)

- L71: discovered_at = models.DateTimeField(default=timezone.now)

- L72: last_checked_at = models.DateTimeField(null=True, blank=True)

- L73: freshness_score = models.PositiveSmallIntegerField(default=50, validators=PERCENT)

- L74: is_active = models.BooleanField(default=True)

- L75: is_expired = models.BooleanField(default=False)

- L76: created_at = models.DateTimeField(auto_now_add=True)

- L77: updated_at = models.DateTimeField(auto_now=True)

- L79: required_skills = models.ManyToManyField("learning.Skill", through="JobSkillRequirement", related_name="job_opportunities")

- L81: class Meta:

- L83: indexes = [

- L84: models.Index(fields=["user", "is_active"]),

- L85: models.Index(fields=["user", "is_remote"]),

- L86: models.Index(fields=["source", "external_id"]),

- L87: models.Index(fields=["user", "company"]),

- L88: models.Index(fields=["user", "location_type"]),

- L89: models.Index(fields=["user", "experience_level"]),

- L90: models.Index(fields=["user", "published_at"]),

- L92: constraints = [

- L93: models.UniqueConstraint(fields=["user", "source", "external_id"], name="jobs_unique_external_per_user_source"),

## job_preference
Source: jobs_opportunity/models/job_preference.py

- L5: class JobPreference(models.Model):

- L6: class RemotePreference(models.TextChoices):

- L12: user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="job_preference")

- L13: target_titles = models.JSONField(default=list, blank=True)

- L14: locations = models.JSONField(default=list, blank=True)

- L15: preferred_job_types = models.JSONField(default=list, blank=True)

- L16: preferred_skills = models.JSONField(default=list, blank=True)

- L17: excluded_companies = models.JSONField(default=list, blank=True)

- L18: preferred_companies = models.JSONField(default=list, blank=True)

- L19: remote_preference = models.CharField(max_length=20, choices=RemotePreference.choices, default=RemotePreference.ANY)

- L20: min_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

- L21: max_salary = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)

- L22: currency = models.CharField(max_length=10, default="USD")

- L23: score_weights = models.JSONField(default=dict, blank=True)

- L24: notification_settings = models.JSONField(default=dict, blank=True)

- L25: created_at = models.DateTimeField(auto_now_add=True)

- L26: updated_at = models.DateTimeField(auto_now=True)

## job_readiness
Source: jobs_opportunity/models/job_readiness.py

- L7: class JobReadiness(models.Model):

- L10: score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L11: level = models.CharField(max_length=30, default="not_ready")

- L12: breakdown = models.JSONField(default=dict, blank=True)

- L13: next_actions = models.JSONField(default=list, blank=True)

- L14: calculated_at = models.DateTimeField(auto_now=True)

- L16: class Meta:

- L17: constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_readiness_unique")]

## job_recommendation
Source: jobs_opportunity/models/job_recommendation.py

- L7: class JobRecommendation(models.Model):

- L10: score = models.PositiveSmallIntegerField(default=0, validators=PERCENT)

- L11: reasons = models.JSONField(default=list, blank=True)

- L12: is_seen = models.BooleanField(default=False)

- L13: is_saved = models.BooleanField(default=False)

- L14: is_dismissed = models.BooleanField(default=False)

- L15: created_at = models.DateTimeField(auto_now_add=True)

- L16: updated_at = models.DateTimeField(auto_now=True)

- L18: class Meta:

- L19: constraints = [models.UniqueConstraint(fields=["user", "job"], name="jobs_user_job_recommendation_unique")]

## job_resume
Source: jobs_opportunity/models/job_resume.py

- L5: class JobResume(models.Model):

- L7: title = models.CharField(max_length=150)

- L8: file = models.FileField(upload_to="jobs/resumes/%Y/%m/", blank=True)

- L9: content = models.TextField(blank=True)

- L10: is_default = models.BooleanField(default=False)

- L11: metadata = models.JSONField(default=dict, blank=True)

- L12: created_at = models.DateTimeField(auto_now_add=True)

- L13: updated_at = models.DateTimeField(auto_now=True)

- L15: class Meta:

## job_saved_search
Source: jobs_opportunity/models/job_saved_search.py

- L5: class JobSavedSearch(models.Model):

- L7: name = models.CharField(max_length=150)

- L8: query = models.CharField(max_length=255, blank=True)

- L9: filters = models.JSONField(default=dict, blank=True)

- L10: alert_enabled = models.BooleanField(default=True)

- L11: last_run_at = models.DateTimeField(null=True, blank=True)

- L12: created_at = models.DateTimeField(auto_now_add=True)

- L13: updated_at = models.DateTimeField(auto_now=True)

## job_skill_gap
Source: jobs_opportunity/models/job_skill_gap.py

- L6: class JobSkillGap(models.Model):

- L7: class Severity(models.TextChoices):

- L13: class Status(models.TextChoices):

- L22: name = models.CharField(max_length=150)

- L23: required_level = models.CharField(max_length=20, default="intermediate")

- L24: current_level = models.CharField(max_length=20, blank=True)

- L25: severity = models.CharField(max_length=20, choices=Severity.choices, default=Severity.MEDIUM)

- L26: status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN)

- L28: metadata = models.JSONField(default=dict, blank=True)

- L29: created_at = models.DateTimeField(auto_now_add=True)

- L30: updated_at = models.DateTimeField(auto_now=True)

- L32: class Meta:

- L33: constraints = [models.UniqueConstraint(fields=["user", "job", "name"], name="jobs_user_job_gap_name_unique")]

- L34: indexes = [models.Index(fields=["user", "status"]), models.Index(fields=["job", "severity"])]

## job_skill_requirement
Source: jobs_opportunity/models/job_skill_requirement.py

- L6: class JobSkillRequirement(models.Model):

- L9: required_level = models.CharField(max_length=20, choices=[(x.value, x.label) for x in __import__("learning.models", fromlist=["Skill"]).Skill.Level], default="intermediate")

- L10: importance = models.PositiveSmallIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(5)])

- L11: requirement_type = models.CharField(max_length=20, choices=[("required", "Required"), ("preferred", "Preferred"), ("optional", "Optional")], default="required")

- L13: class Meta:

- L14: constraints = [models.UniqueConstraint(fields=["job", "skill"], name="jobs_job_skill_unique")]

## job_source
Source: jobs_opportunity/models/job_source.py

- L5: class JobSource(models.Model):

- L6: class SourceType(models.TextChoices):

- L13: name = models.CharField(max_length=150)

- L14: source_type = models.CharField(max_length=20, choices=SourceType.choices, default=SourceType.MANUAL)

- L15: base_url = models.URLField(blank=True)

- L16: feed_url = models.URLField(blank=True)

- L17: enabled = models.BooleanField(default=True)

- L18: sync_interval_minutes = models.PositiveIntegerField(default=60)

- L19: max_items_per_sync = models.PositiveIntegerField(default=100)

- L20: config = models.JSONField(default=dict, blank=True)

- L21: last_synced_at = models.DateTimeField(null=True, blank=True)

- L22: last_sync_status = models.CharField(max_length=20, default="never")

- L23: last_sync_error = models.TextField(blank=True)

- L24: last_sync_count = models.PositiveIntegerField(default=0)

- L25: created_at = models.DateTimeField(auto_now_add=True)

- L26: updated_at = models.DateTimeField(auto_now=True)

- L28: class Meta:

- L30: constraints = [models.UniqueConstraint(fields=["user", "name"], name="jobs_source_user_name_unique")]

## job_source_sync_run
Source: jobs_opportunity/models/job_source_sync_run.py

- L6: class JobSourceSyncRun(models.Model):

- L7: class Status(models.TextChoices):

- L16: celery_task_id = models.CharField(max_length=255, blank=True, default="")

- L17: status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED)

- L18: started_at = models.DateTimeField(null=True, blank=True)

- L19: finished_at = models.DateTimeField(null=True, blank=True)

- L20: job_count = models.PositiveIntegerField(default=0)

- L21: error_message = models.TextField(blank=True, default="")

- L22: metadata = models.JSONField(default=dict, blank=True)

- L23: created_at = models.DateTimeField(auto_now_add=True)

- L25: class Meta:

- L27: indexes = [

- L28: models.Index(fields=["user", "-created_at"]),

- L29: models.Index(fields=["source", "-created_at"]),

- L30: models.Index(fields=["status"]),

## __init__
Source: jobs_opportunity/models/__init__.py


Cross-app references and ownership must be confirmed from fields and write paths. See [project data catalog](../../06-database-and-model-catalog.md).
