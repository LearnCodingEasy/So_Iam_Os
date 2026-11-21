from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from learning.models.assessment import Assessment
from learning.models.common import SCORE_VALIDATORS


class AssessmentAttempt(models.Model):
    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="attempts",
    )
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="assessment_attempts",
    )

    score = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=SCORE_VALIDATORS,
    )
    passed = models.BooleanField(default=False)
    feedback = models.TextField(blank=True)

    started_at = models.DateTimeField(default=timezone.now)
    completed_at = models.DateTimeField(null=True, blank=True)
    attempt_number = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["-started_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["assessment", "user", "attempt_number"],
                name="unique_assessment_attempt_number",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "assessment", "started_at"]),
        ]

    def clean(self):
        super().clean()
        if self.completed_at and self.completed_at < self.started_at:
            raise ValidationError(
                {"completed_at": "Cannot precede start time."}
            )

    def __str__(self):
        return f"{self.user} - {self.assessment} - {self.score}"
