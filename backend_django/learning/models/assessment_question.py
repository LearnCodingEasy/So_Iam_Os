from django.db import models
from learning.models.assessment import Assessment


class AssessmentQuestion(models.Model):
    class Type(models.TextChoices):
        SINGLE_CHOICE = "single_choice", "Single choice"
        MULTIPLE_SELECT = "multiple_select", "Multiple select"
        TRUE_FALSE = "true_false", "True / False"
        SHORT_ANSWER = "short_answer", "Short answer"
        PRACTICAL = "practical", "Practical task"

    assessment = models.ForeignKey(
        Assessment,
        on_delete=models.CASCADE,
        related_name="questions",
    )
    question_type = models.CharField(
        max_length=30,
        choices=Type.choices,
    )
    prompt = models.TextField()
    explanation = models.TextField(blank=True)
    points = models.PositiveIntegerField(default=1)
    order = models.PositiveIntegerField(default=0)
    is_required = models.BooleanField(default=True)

    # Private grading data; exclude from learner serializers.
    grading_data = models.JSONField(default=dict, blank=True)

    class Meta:
        ordering = ["order", "id"]
        indexes = [
            models.Index(fields=["assessment", "order"]),
        ]

    def __str__(self):
        return f"{self.assessment}: Q{self.order}"
