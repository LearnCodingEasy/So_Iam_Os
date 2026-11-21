
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
