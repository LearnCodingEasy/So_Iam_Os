from rest_framework import serializers
from codex.models import CodexToolDefinition


class ToolDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexToolDefinition
        fields = "__all__"
