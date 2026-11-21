
from rest_framework import serializers

from ai.models import AIExecution, AIBudgetPolicy, AiAuditLog


class AIExecutionSerializer(serializers.ModelSerializer):

    class Meta:
        model = AIExecution

        fields = [
            "id",
            "agent",
            "task_type",
            "requested_provider",
            "provider",
            "model",
            "status",
            "started_at",
            "finished_at",
            "duration_ms",
            "retry_count",
            "fallback_count",
            "genuine_result",
            "error_code",
            "error_message",
            "metadata",
            "created_at",
        ]


class AIBudgetPolicySerializer(serializers.ModelSerializer):

    class Meta:
        model = AIBudgetPolicy

        fields = [
            "id",
            "scope",
            "scope_key",
            "daily_cost_limit",
            "monthly_cost_limit",
            "daily_token_limit",
            "monthly_token_limit",
            "enabled",
            "updated_at",
        ]


class AiAuditLogSerializer(serializers.ModelSerializer):
    result = serializers.SerializerMethodField()

    class Meta:
        model = AiAuditLog
        fields = ["id", "action", "resource", "result", "details", "ip_address", "created_at"]
        read_only_fields = fields

    def get_result(self, obj):
        return (obj.details or {}).get("result", "")
