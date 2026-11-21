from rest_framework import serializers
from codex.models import CodexAgentDefinition


class AgentDefinitionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexAgentDefinition
        fields = "__all__"
