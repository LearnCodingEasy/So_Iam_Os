from django.conf import settings
from django.db import models


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
