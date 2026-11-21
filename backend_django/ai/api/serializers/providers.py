
from rest_framework import serializers

from ai.models import AIProviderCredential


class AIProviderTestSerializer(serializers.Serializer):
    model = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=255,
    )


class AIProviderCredentialSerializer(serializers.ModelSerializer):
    has_api_key = serializers.BooleanField(read_only=True)
    base_url = serializers.CharField(required=False, allow_blank=True, write_only=False)
    model = serializers.CharField(required=False, allow_blank=True, write_only=False)
    priority = serializers.IntegerField(required=False, min_value=1, max_value=999, write_only=False)
    enabled = serializers.BooleanField(required=False, write_only=False)

    api_key = serializers.CharField(
        write_only=True,
        required=False,
        allow_blank=False,
        trim_whitespace=True,
    )

    class Meta:
        model = AIProviderCredential

        fields = [
            "id",
            "provider",
            "has_api_key",
            "api_key",
            "metadata",
            "base_url",
            "model",
            "priority",
            "enabled",
            "status",
            "last_used_at",
            "last_validated_at",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "has_api_key",
            "status",
            "last_used_at",
            "last_validated_at",
            "created_at",
            "updated_at",
        ]

    def to_representation(self, instance):
        data = super().to_representation(instance)
        metadata = dict(instance.metadata or {})
        data["base_url"] = metadata.get("base_url", "")
        data["model"] = metadata.get("model", "")
        data["priority"] = metadata.get("priority", 100)
        data["enabled"] = metadata.get("enabled", True)
        # Never expose arbitrary metadata that could accidentally contain secrets.
        data["metadata"] = {k: v for k, v in metadata.items() if k in {"priority", "enabled", "base_url", "model"}}
        return data

    def _merge_metadata(self, validated_data):
        keys = {"base_url", "model", "priority", "enabled"}
        supplied = validated_data.get("metadata") or {}
        if not isinstance(supplied, dict):
            raise serializers.ValidationError({"metadata": "Metadata must be an object."})
        metadata = {key: value for key, value in supplied.items() if key in keys}
        for key in keys:
            if key in validated_data:
                metadata[key] = validated_data.pop(key)
        validated_data.pop("metadata", None)
        return metadata

    def create(self, validated_data):
        api_key = validated_data.pop("api_key", "")
        provider = validated_data.pop("provider")
        metadata = self._merge_metadata(validated_data)
        user = self.context["request"].user

        # Credential POST is an upsert. Preserve existing metadata and secrets
        # when a caller updates only one field or resubmits provider settings.
        obj, created = AIProviderCredential.objects.get_or_create(
            user=user,
            provider=provider,
            defaults={"metadata": metadata},
        )
        changed_fields = []
        if metadata:
            obj.metadata = {**(obj.metadata or {}), **metadata}
            changed_fields.append("metadata")
        if api_key:
            obj.set_api_key(api_key)
            changed_fields.append("encrypted_api_key")
        if changed_fields:
            obj.save(update_fields=[*changed_fields, "updated_at"])
        return obj

    def update(self, instance, validated_data):
        api_key = validated_data.pop("api_key", None)
        metadata = self._merge_metadata(validated_data)
        if metadata:
            validated_data["metadata"] = {**(instance.metadata or {}), **metadata}

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if api_key:
            instance.set_api_key(api_key)

        instance.save()

        return instance
