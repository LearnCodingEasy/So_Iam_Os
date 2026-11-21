from rest_framework import serializers
from learning.models import AssessmentChoice, AssessmentResponse
from learning.api.serializers.common import get_request_user


# ===================================================
# Assessment Response
# ===================================================


class AssessmentResponseSerializer(
    serializers.ModelSerializer
):
    selected_choices = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=AssessmentChoice.objects.all(),
        required=False,
    )

    class Meta:
        model = AssessmentResponse
        fields = (
            "id",
            "attempt",
            "question",
            "selected_choices",
            "text_answer",
            "is_correct",
            "points_awarded",
            "feedback",
        )
        read_only_fields = (
            "id",
            "is_correct",
            "points_awarded",
            "feedback",
        )

    def validate(self, attrs):
        user = get_request_user(self)

        if user is None:
            raise serializers.ValidationError(
                "Authentication is required."
            )

        attempt = attrs.get(
            "attempt",
            self.instance.attempt
            if self.instance
            else None,
        )

        question = attrs.get(
            "question",
            self.instance.question
            if self.instance
            else None,
        )

        if attempt and attempt.user_id != user.id:
            raise serializers.ValidationError(
                {
                    "attempt": (
                        "This attempt does not belong "
                        "to the current user."
                    )
                }
            )

        if attempt and question:
            if (
                attempt.assessment_id
                != question.assessment_id
            ):
                raise serializers.ValidationError(
                    {
                        "question": (
                            "Question must belong to "
                            "the attempt's assessment."
                        )
                    }
                )

        selected_choices = attrs.get(
            "selected_choices"
        )

        if selected_choices and question:
            invalid_choices = [
                choice.id
                for choice in selected_choices
                if choice.question_id != question.id
            ]

            if invalid_choices:
                raise serializers.ValidationError(
                    {
                        "selected_choices": (
                            "All selected choices must "
                            "belong to the selected question."
                        )
                    }
                )

        return attrs
