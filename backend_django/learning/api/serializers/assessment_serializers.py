from rest_framework import serializers
from learning.models import Assessment
from learning.api.serializers.assessment_question_serializers import AssessmentQuestionLearnerSerializer, AssessmentQuestionSerializer
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Assessment
# ===================================================


class AssessmentSerializer(serializers.ModelSerializer):
    assessment_type_display = serializers.CharField(
        source="get_assessment_type_display",
        read_only=True,
    )

    questions = AssessmentQuestionSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Assessment
        fields = (
            "id",
            "topic",
            "title",
            "description",
            "instructions",
            "assessment_type",
            "assessment_type_display",
            "passing_score",
            "estimated_minutes",
            "order",
            "is_active",
            "questions",
            "created_at",
            "updated_at",
        )
        read_only_fields = (
            "id",
            "assessment_type_display",
            "questions",
            "created_at",
            "updated_at",
        )

    def validate_topic(self, topic):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        ensure_owner(
            user,
            topic.path,
            "topic",
        )

        return topic


class AssessmentLearnerSerializer(
    serializers.ModelSerializer
):
    """
    Safe assessment serializer for the learner UI.
    """

    assessment_type_display = serializers.CharField(
        source="get_assessment_type_display",
        read_only=True,
    )

    questions = AssessmentQuestionLearnerSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Assessment
        fields = (
            "id",
            "topic",
            "title",
            "description",
            "instructions",
            "assessment_type",
            "assessment_type_display",
            "passing_score",
            "estimated_minutes",
            "order",
            "is_active",
            "questions",
        )
        read_only_fields = fields
