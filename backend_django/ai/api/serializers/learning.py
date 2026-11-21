
from rest_framework import serializers


class AILearningTopicSerializer(serializers.Serializer):

    title = serializers.CharField(
        max_length=255,
        allow_blank=False,
        trim_whitespace=True,
    )

    description = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )

    order = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=100,
    )

    estimated_minutes = serializers.IntegerField(
        required=False,
        min_value=0,
        max_value=10000,
    )


class AILearningPlanSerializer(serializers.Serializer):

    intent = serializers.ChoiceField(
        choices=[
            ("create_learning_plan", "Create Learning Plan")
        ]
    )

    skill = serializers.CharField(
        max_length=255,
        allow_blank=False,
        trim_whitespace=True,
    )

    level = serializers.ChoiceField(
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
            ("expert", "Expert"),
        ],
        default="beginner",
    )

    target_level = serializers.ChoiceField(
        choices=[
            ("beginner", "Beginner"),
            ("intermediate", "Intermediate"),
            ("advanced", "Advanced"),
            ("expert", "Expert"),
        ],
        default="advanced",
    )

    goal_title = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
        default="",
    )

    goal_description = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )

    path_title = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
        default="",
    )

    path_description = serializers.CharField(
        required=False,
        allow_blank=True,
        default="",
    )

    topics = AILearningTopicSerializer(
        many=True,
        required=False,
    )

    def validate_topics(self, value):
        if len(value) > 30:
            raise serializers.ValidationError(
                "A learning plan cannot contain more than 30 topics."
            )

        return value
