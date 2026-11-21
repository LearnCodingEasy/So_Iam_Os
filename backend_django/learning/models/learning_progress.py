from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q
from learning.models.common import SCORE_VALIDATORS
from learning.models.learning_topic import LearningTopic


PERCENT_VALIDATORS = [
    MinValueValidator(0),
    MaxValueValidator(100),
]


class LearningProgress(models.Model):
    class Mastery(models.TextChoices):
        NOT_STARTED = "not_started", "Not Started"
        BEGINNER = "beginner", "Beginner"
        DEVELOPING = "developing", "Developing"
        COMPETENT = "competent", "Competent"
        ADVANCED = "advanced", "Advanced"
        MASTERED = "mastered", "Mastered"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_progress",
    )
    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="progress_records",
    )

    progress_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=PERCENT_VALIDATORS,
    )
    practice_completed = models.BooleanField(default=False)

    # Legacy field retained during migration.
    notes = models.TextField(blank=True)

    mastery_level = models.CharField(
        max_length=20,
        choices=Mastery.choices,
        default=Mastery.NOT_STARTED,
    )
    last_ai_score = models.FloatField(
        null=True,
        blank=True,
        validators=SCORE_VALIDATORS,
    )
    needs_review = models.BooleanField(default=False)

    lesson_completed = models.BooleanField(default=False)
    quick_check_completed = models.BooleanField(default=False)
    assessment_completed = models.BooleanField(default=False)

    last_activity_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-updated_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["topic", "user"],
                name="unique_learning_progress_per_user_topic",
            ),
            models.CheckConstraint(
                condition=Q(progress_percent__gte=0)
                & Q(progress_percent__lte=100),
                name="learning_progress_percent_0_100",
            ),
        ]
        indexes = [
            models.Index(fields=["user", "needs_review"]),
            models.Index(fields=["user", "last_activity_at"]),
        ]

    def __str__(self):
        return f"{self.user} - {self.topic} - {self.progress_percent}%"
