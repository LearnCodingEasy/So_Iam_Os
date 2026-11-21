from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from learning.models.application_submission import ApplicationSubmission
from learning.models.common import SCORE_VALIDATORS
from learning.models.knowledge_application import KnowledgeApplication


class ApplicationReview(models.Model):
    class Mastery(models.TextChoices):
        BEGINNER = "beginner", "Beginner"
        DEVELOPING = "developing", "Developing"
        COMPETENT = "competent", "Competent"
        ADVANCED = "advanced", "Advanced"
        MASTERED = "mastered", "Mastered"

    submission = models.ForeignKey(
        ApplicationSubmission,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    # Compatibility link to the parent application.
    application = models.ForeignKey(
        KnowledgeApplication,
        on_delete=models.CASCADE,
        related_name="reviews",
    )

    score = models.FloatField(validators=SCORE_VALIDATORS)
    mastery_level = models.CharField(
        max_length=20,
        choices=Mastery.choices,
        default=Mastery.DEVELOPING,
    )

    understood = models.JSONField(default=list, blank=True)
    applied = models.JSONField(default=list, blank=True)
    strengths = models.JSONField(default=list, blank=True)
    weaknesses = models.JSONField(default=list, blank=True)
    errors = models.JSONField(default=list, blank=True)
    needs_review = models.JSONField(default=list, blank=True)
    knowledge_gaps = models.JSONField(default=list, blank=True)
    recommendations = models.JSONField(default=list, blank=True)

    feedback = models.TextField(blank=True)
    ai_metadata = models.JSONField(default=dict, blank=True)
    reviewed_by = models.CharField(max_length=100, default="ai")
    reviewed_at = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-reviewed_at"]
        indexes = [
            models.Index(fields=["application", "reviewed_at"]),
        ]

    def clean(self):
        super().clean()
        if self.submission_id and self.application_id:
            if self.submission.application_id != self.application_id:
                raise ValidationError(
                    "Submission must belong to this application."
                )

    def __str__(self):
        return f"Review: {self.application.title}"
