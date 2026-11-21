from rest_framework import serializers
from learning.models import AssessmentChoice


# ===================================================
# Assessment Choice
# ===================================================


class AssessmentChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssessmentChoice
        fields = (
            "id",
            "question",
            "text",
            "order",
            "feedback",
        )
        read_only_fields = (
            "id",
        )


class AssessmentChoiceLearnerSerializer(
    serializers.ModelSerializer
):
    """
    Learner-facing choice serializer.

    IMPORTANT:
    is_correct is intentionally excluded.
    """

    class Meta:
        model = AssessmentChoice
        fields = (
            "id",
            "text",
            "order",
        )
        read_only_fields = fields
