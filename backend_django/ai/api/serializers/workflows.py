
from rest_framework import serializers

from ai.models import AIWorkflowDefinition


class AIWorkflowDefinitionSerializer(serializers.ModelSerializer):

    user = serializers.HiddenField(
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        model = AIWorkflowDefinition

        fields = [
            "id",
            "user",
            "name",
            "description",
            "graph",
            "version",
            "is_active",
            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "version",
            "created_at",
            "updated_at",
        ]

        validators = []

    def validate_graph(self, value):
        from ai.services.workflow_service import WorkflowService

        result = WorkflowService.validate(value)

        if not result.get("valid"):
            raise serializers.ValidationError(
                result.get(
                    "errors",
                    ["Invalid workflow graph."]
                )
            )

        return value
