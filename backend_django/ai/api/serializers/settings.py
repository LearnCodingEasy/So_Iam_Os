
from rest_framework import serializers

from ai.models import AISettings


class AISettingsSerializer(serializers.ModelSerializer):

    class Meta:
        model = AISettings

        fields = [
            "preferred_provider",
            "preferred_model",
            "default_prompt_profile",
            "context_enabled",
            "streaming_enabled",
            "temperature",
            "timeout_seconds",
            "fallback_enabled",
            "max_context_tokens",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "created_at",
            "updated_at",
        ]

    def validate_timeout_seconds(self, value):
        from ai.services.timeouts import validate_timeout
        try:
            return validate_timeout(value, field="timeout_seconds")
        except ValueError as exc:
            raise serializers.ValidationError(str(exc))

    def validate_default_prompt_profile(self, value):
        request = self.context.get("request")

        if (
            value
            and request
            and value.user_id != request.user.id
        ):
            raise serializers.ValidationError(
                "Prompt profile does not belong to the current user."
            )

        return value
