from django.db import models
from django.utils import timezone
from jobs_opportunity.models.job_application import JobApplication


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
