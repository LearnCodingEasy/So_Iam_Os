from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from jobs_opportunity.models.job_application import JobApplication


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
