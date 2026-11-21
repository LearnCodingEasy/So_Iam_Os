from django.conf import settings
from django.db import models


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
