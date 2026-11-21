from django.conf import settings
from django.db import models
from jobs_opportunity.models.job_opportunity import JobOpportunity
from jobs_opportunity.models.job_resume import JobResume


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
