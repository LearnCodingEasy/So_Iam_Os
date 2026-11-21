from django.conf import settings
from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
from learning.models.common import MINUTES_VALIDATORS
from learning.models.learning_topic import LearningTopic
from learning.models.lesson import Lesson


class LearningSession(models.Model):
    class ActivityType(models.TextChoices):
        LESSON = "lesson", "Lesson"
        PRACTICE = "practice", "Practice"
        ASSESSMENT = "assessment", "Assessment"
        REVIEW = "review", "Review"
        READING = "reading", "Reading"
        OTHER = "other", "Other"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="learning_sessions",
    )
    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="sessions",
    )
    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="sessions",
    )

    activity_type = models.CharField(
        max_length=20,
        choices=ActivityType.choices,
        default=ActivityType.LESSON,
    )
    started_at = models.DateTimeField(default=timezone.now)
    ended_at = models.DateTimeField(null=True, blank=True)
    duration_seconds = models.PositiveIntegerField(
        default=0,
        validators=MINUTES_VALIDATORS,
    )
    completed = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["-started_at"]
        indexes = [
            models.Index(fields=["user", "started_at"]),
            models.Index(fields=["topic", "started_at"]),
        ]

    def clean(self):
        super().clean()
        if self.ended_at and self.ended_at < self.started_at:
            raise ValidationError(
                {"ended_at": "End time cannot precede start time."}
            )
        if self.lesson_id and self.topic_id:
            if self.lesson.topic_id != self.topic_id:
                raise ValidationError(
                    {"lesson": "Lesson must belong to this topic."}
                )

    def __str__(self):
        return f"{self.user} - {self.topic} - {self.started_at}"
