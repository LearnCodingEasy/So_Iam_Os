
from rest_framework import serializers

from ai.models import AIPromptProfile


class AIPromptProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIPromptProfile

        fields = [
            "id",
            "name",
            "system_prompt",
            "context_instructions",
            "temperature",
            "max_tokens",
            "is_default",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "created_at",
            "updated_at",
        ]

    def validate_temperature(self, value):
        if value is not None and not 0 <= value <= 2:
            raise serializers.ValidationError(
                "Temperature must be between 0 and 2."
            )

        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if user and attrs.get("is_default"):
            # Default profile management should happen atomically
            # at the service layer.

            pass

        return attrs


