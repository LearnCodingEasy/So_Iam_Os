from rest_framework import serializers
from learning.models import AssessmentAttempt
from learning.api.serializers.assessment_serializers import AssessmentLearnerSerializer
from learning.api.serializers.common import ensure_owner, get_request_user


# ===================================================
# Assessment Attempt
# ===================================================


class AssessmentAttemptSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    assessment_detail = AssessmentLearnerSerializer(
        source="assessment",
        read_only=True,
    )

    class Meta:
        model = AssessmentAttempt
        fields = (
            "id",
            "assessment",
            "assessment_detail",
            "user",
            "score",
            "passed",
            "feedback",
            "started_at",
            "completed_at",
            "attempt_number",
        )
        read_only_fields = (
            "id",
            "user",
            "score",
            "passed",
            "feedback",
            "completed_at",
            "attempt_number",
        )

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

    def create(self, validated_data):
        user = get_request_user(self)

        assessment = validated_data["assessment"]

        last_attempt = (
            AssessmentAttempt.objects
            .filter(
                assessment=assessment,
                user=user,
            )
            .order_by("-attempt_number")
            .first()
        )

        next_attempt_number = (
            last_attempt.attempt_number + 1
            if last_attempt
            else 1
        )

        return AssessmentAttempt.objects.create(
            user=user,
            attempt_number=next_attempt_number,
            **validated_data,
        )
