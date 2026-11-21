
from django.conf import settings
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator


class AIFeedback(models.Model):

    class Sentiment(models.TextChoices):
        LIKE = "like", "Like"
        DISLIKE = "dislike", "Dislike"

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="ai_feedback"
    )

    message = models.ForeignKey(
        "ai.AIMessage",
        on_delete=models.CASCADE,
        related_name="feedback"
    )

    sentiment = models.CharField(
        max_length=10,
        choices=Sentiment.choices
    )

    reason = models.CharField(
        max_length=255,
        blank=True,
        default=""
    )

    comment = models.TextField(
        blank=True,
        default=""
    )

    feedback_category = models.CharField(
        max_length=80,
        blank=True,
        default=""
    )

    model_version = models.CharField(
        max_length=120,
        blank=True,
        default=""
    )

    reviewed_at = models.DateTimeField(
        null=True,
        blank=True
    )

    rating = models.PositiveSmallIntegerField(
        null=True,
        blank=True,
        validators=[
            MinValueValidator(1),
            MaxValueValidator(5)
        ]
    )

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "message"],
                name="unique_ai_feedback_user_message"
            )
        ]

        indexes = [
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["sentiment", "-created_at"]),
        ]

    def __str__(self):
        return f"{self.user_id} - {self.sentiment}"
