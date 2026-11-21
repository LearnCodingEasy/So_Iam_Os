from django.db import models
from django.db.models import Q
from learning.models.common import MINUTES_VALIDATORS, SCORE_VALIDATORS
from learning.models.learning_topic import LearningTopic


class Assessment(models.Model):
    class Type(models.TextChoices):
        QUIZ = "quiz", "Quiz"
        QUICK_CHECK = "quick_check", "Quick Check"
        PRACTICAL = "practical", "Practical"
        PROJECT = "project", "Project"

    topic = models.ForeignKey(
        LearningTopic,
        on_delete=models.CASCADE,
        related_name="assessments",
    )
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    instructions = models.TextField(blank=True)

    assessment_type = models.CharField(
        max_length=20,
        choices=Type.choices,
        default=Type.QUIZ,
    )
    passing_score = models.PositiveSmallIntegerField(
        default=70,
        validators=SCORE_VALIDATORS,
    )
    estimated_minutes = models.PositiveIntegerField(
        default=0,
        validators=MINUTES_VALIDATORS,
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["order", "created_at"]
        indexes = [
            models.Index(fields=["topic", "assessment_type", "is_active"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(passing_score__gte=0)
                & Q(passing_score__lte=100),
                name="assessment_passing_score_0_100",
            ),
        ]

    def __str__(self):
        return self.title
