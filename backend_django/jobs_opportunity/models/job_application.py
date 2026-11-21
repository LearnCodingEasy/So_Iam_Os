from django.conf import settings
from django.db import models
from jobs_opportunity.models.job_opportunity import JobOpportunity


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
