
from rest_framework import serializers


class AIFeedbackSerializer(serializers.Serializer):

    message_id = serializers.IntegerField(
        min_value=1
    )

    sentiment = serializers.ChoiceField(
        choices=[
            ("like", "Like"),
            ("dislike", "Dislike"),
        ]
    )

    reason = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )

    comment = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=5000,
    )

    feedback_category = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=80,
    )

    rating = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=5,
    )
