from rest_framework import serializers
from learning.models import AssessmentQuestion
from learning.api.serializers.assessment_choice_serializers import AssessmentChoiceLearnerSerializer, AssessmentChoiceSerializer
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Assessment Question
# ===================================================


class AssessmentQuestionSerializer(serializers.ModelSerializer):
    question_type_display = serializers.CharField(
        source="get_question_type_display",
        read_only=True,
    )

    choices = AssessmentChoiceSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AssessmentQuestion
        fields = (
            "id",
            "assessment",
            "question_type",
            "question_type_display",
            "prompt",
            "explanation",
            "points",
            "order",
            "is_required",
            "grading_data",
            "choices",
        )
        read_only_fields = (
            "id",
            "question_type_display",
            "choices",
        )

        extra_kwargs = {
            "grading_data": {
                "write_only": True,
            },
        }

    def validate_assessment(self, assessment):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            assessment.topic.path,
            "assessment",
        )

        return assessment


class AssessmentQuestionLearnerSerializer(
    serializers.ModelSerializer
):
    """
    Safe serializer used while the learner is taking an assessment.

    Never exposes:
    - grading_data
    - correct answers
    """

    question_type_display = serializers.CharField(
        source="get_question_type_display",
        read_only=True,
    )

    choices = AssessmentChoiceLearnerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = AssessmentQuestion
        fields = (
            "id",
            "assessment",
            "question_type",
            "question_type_display",
            "prompt",
            "explanation",
            "points",
            "order",
            "is_required",
            "choices",
        )
        read_only_fields = fields
