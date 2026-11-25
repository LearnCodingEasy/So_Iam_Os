
from rest_framework import serializers

from ai.models import AIConversation, AIMessage, AISettings


class AIMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMessage
        fields = [
            "id",
            "role",
            "content",
            "provider",
            "model",
            "metadata",
            "created_at",
        ]


class AIConversationSerializer(serializers.ModelSerializer):
    messages = AIMessageSerializer(many=True, read_only=True)

    class Meta:
        model = AIConversation
        fields = [
            "id",
            "title",
            "provider",
            "model",
            "is_active",
            "archived_at",
            "deleted_at",
            "last_message_at",
            "message_count",
            "metadata",
            "created_at",
            "updated_at",
            "messages",
        ]


class AIChatSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=True,
        allow_blank=False,
        trim_whitespace=True,
    )

    conversation_id = serializers.IntegerField(
        required=False,
        allow_null=True,
    )

    provider = serializers.ChoiceField(
        choices=AISettings.Provider.choices,
        required=False,
    )

    model = serializers.CharField(
        required=False,
        allow_blank=True,
    )

    system_prompt = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=8000,
    )

    temperature = serializers.FloatField(
        required=False,
        min_value=0,
        max_value=2,
    )

    max_tokens = serializers.IntegerField(
        required=False,
        min_value=1,
        max_value=200000,
    )

    idempotency_key = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )

    # Per-request wait for the provider, in seconds. "timeout" is the public
    # name; "timeout_seconds" is accepted as an alias. Bounds are enforced
    # server-side from settings (AI_TIMEOUT_MIN/MAX_SECONDS).
    timeout = serializers.IntegerField(required=False, allow_null=True)
    timeout_seconds = serializers.IntegerField(required=False, allow_null=True)

    def _check_timeout(self, value):
        from ai.services.timeouts import validate_timeout
        if value is None:
            return value
        try:
            return validate_timeout(value)
        except ValueError as exc:
            raise serializers.ValidationError(str(exc))

    def validate_timeout(self, value):
        return self._check_timeout(value)

    def validate_timeout_seconds(self, value):
        return self._check_timeout(value)

    def validate(self, attrs):
        # Normalise: expose a single effective request timeout.
        effective = attrs.get("timeout")
        if effective is None:
            effective = attrs.get("timeout_seconds")
        attrs["timeout"] = effective
        attrs.pop("timeout_seconds", None)
        return attrs
