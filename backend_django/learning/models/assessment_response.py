from django.core.exceptions import ValidationError
from django.db import models
from learning.models.assessment_attempt import AssessmentAttempt
from learning.models.assessment_choice import AssessmentChoice
from learning.models.assessment_question import AssessmentQuestion


class AssessmentResponse(models.Model):
    attempt = models.ForeignKey(
        AssessmentAttempt,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    question = models.ForeignKey(
        AssessmentQuestion,
        on_delete=models.CASCADE,
        related_name="responses",
    )
    selected_choices = models.ManyToManyField(
        AssessmentChoice,
        blank=True,
        related_name="responses",
    )
    text_answer = models.TextField(blank=True)
    is_correct = models.BooleanField(null=True, blank=True)
    points_awarded = models.FloatField(default=0)
    feedback = models.TextField(blank=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["attempt", "question"],
                name="unique_response_per_attempt_question",
            ),
        ]

    def clean(self):
        super().clean()
        if self.attempt_id and self.question_id:
            if self.attempt.assessment_id != self.question.assessment_id:
                raise ValidationError(
                    "Question must belong to the attempt's assessment."
                )

    def __str__(self):
        return f"Response: {self.question_id}"
