from rest_framework import serializers
from codex.models import LocalAIJob


class LocalAIJobSerializer(serializers.ModelSerializer):
    class Meta:
        model = LocalAIJob
        fields = "__all__"
        read_only_fields = ["user", "status", "provider", "result", "error", "started_at", "completed_at", "created_at"]
