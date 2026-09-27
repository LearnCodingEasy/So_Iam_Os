from rest_framework import serializers

from .models import AIConversation, AIMessage, AISettings, AIProviderCredential, AIPromptProfile


class AIMessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIMessage
        fields = ["id", "role", "content", "provider",
                  "model", "metadata", "created_at"]


class AIConversationSerializer(serializers.ModelSerializer):
    messages = AIMessageSerializer(many=True, read_only=True)

    class Meta:
        model = AIConversation
        fields = ["id", "title", "provider", "model", "is_active",
                  "metadata", "created_at", "updated_at", "messages"]


class AIChatSerializer(serializers.Serializer):
    message = serializers.CharField(
        required=True, allow_blank=False, trim_whitespace=True)
    conversation_id = serializers.IntegerField(required=False, allow_null=True)
    provider = serializers.ChoiceField(
        choices=AISettings.Provider.choices, required=False)
    model = serializers.CharField(required=False, allow_blank=True)


class AISettingsSerializer(serializers.ModelSerializer):
    class Meta:
        model = AISettings
        fields = ["preferred_provider", "preferred_model", "default_prompt_profile",
                  "context_enabled", "max_context_tokens", "created_at", "updated_at"]
        read_only_fields = ["created_at", "updated_at"]

    def validate_default_prompt_profile(self, value):
        if value and value.user_id != self.context["request"].user.id:
            raise serializers.ValidationError(
                "Prompt profile does not belong to the current user.")
        return value


class AIProviderCredentialSerializer(serializers.ModelSerializer):
    has_api_key = serializers.BooleanField(read_only=True)
    api_key = serializers.CharField(
        write_only=True, required=False, allow_blank=False, trim_whitespace=True)

    class Meta:
        model = AIProviderCredential
        fields = ["id", "provider", "has_api_key", "api_key",
                  "metadata", "created_at", "updated_at"]
        read_only_fields = ["id", "has_api_key", "created_at", "updated_at"]

    def create(self, validated_data):
        api_key = validated_data.pop("api_key", "")
        obj, _ = AIProviderCredential.objects.update_or_create(
            user=self.context["request"].user,
            provider=validated_data["provider"],
            defaults=validated_data,
        )
        if api_key:
            obj.set_api_key(api_key)
            obj.save(update_fields=["encrypted_api_key", "updated_at"])
        return obj

    def update(self, instance, validated_data):
        api_key = validated_data.pop("api_key", None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if api_key:
            instance.set_api_key(api_key)
        instance.save()
        return instance


class AIPromptProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AIPromptProfile
        fields = ["id", "name", "system_prompt", "context_instructions",
                  "temperature", "max_tokens", "is_default", "created_at", "updated_at"]
        read_only_fields = ["id", "created_at", "updated_at"]

    def validate_temperature(self, value):
        if value is not None and not 0 <= value <= 2:
            raise serializers.ValidationError(
                "Temperature must be between 0 and 2.")
        return value


class AILearningTopicSerializer(serializers.Serializer):
    title = serializers.CharField(
        max_length=255, allow_blank=False, trim_whitespace=True)
    description = serializers.CharField(
        required=False, allow_blank=True, default="")
    order = serializers.IntegerField(
        required=False, min_value=1, max_value=100)
    estimated_minutes = serializers.IntegerField(
        required=False, min_value=0, max_value=10000)


class AILearningPlanSerializer(serializers.Serializer):
    intent = serializers.ChoiceField(
        choices=[("create_learning_plan", "Create Learning Plan")])
    skill = serializers.CharField(
        max_length=255, allow_blank=False, trim_whitespace=True)
    level = serializers.ChoiceField(choices=[("beginner", "Beginner"), ("intermediate", "Intermediate"), (
        "advanced", "Advanced"), ("expert", "Expert")], default="beginner")
    target_level = serializers.ChoiceField(choices=[("beginner", "Beginner"), (
        "intermediate", "Intermediate"), ("advanced", "Advanced"), ("expert", "Expert")], default="advanced")
    goal_title = serializers.CharField(
        required=False, allow_blank=True, max_length=255, default="")
    goal_description = serializers.CharField(
        required=False, allow_blank=True, default="")
    reason = serializers.CharField(
        required=False, allow_blank=True, default="")
    path_title = serializers.CharField(
        required=False, allow_blank=True, max_length=255, default="")
    path_description = serializers.CharField(
        required=False, allow_blank=True, default="")
    topics = AILearningTopicSerializer(many=True, required=False)

    def validate_topics(self, value):
        if len(value) > 30:
            raise serializers.ValidationError(
                "A learning plan cannot contain more than 30 topics.")
        return value
