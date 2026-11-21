from rest_framework import serializers
from codex.models import CodexWorkflowStep


class WorkflowStepSerializer(serializers.ModelSerializer):
    class Meta:
        model = CodexWorkflowStep
        fields = "__all__"
        read_only_fields = ["completed_at", "updated_at"]
