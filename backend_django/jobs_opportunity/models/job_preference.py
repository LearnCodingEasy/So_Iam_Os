from django.conf import settings
from django.db import models


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
