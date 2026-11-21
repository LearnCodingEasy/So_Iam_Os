from django.db import models
from learning.models.assessment_question import AssessmentQuestion


class AssessmentChoice(models.Model):
    question = models.ForeignKey(
        AssessmentQuestion,
        on_delete=models.CASCADE,
        related_name="choices",
    )
    text = models.TextField()
    order = models.PositiveIntegerField(default=0)

    # Never expose this field in learner-facing serializers.
    is_correct = models.BooleanField(default=False)

    feedback = models.TextField(blank=True)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text[:100]
