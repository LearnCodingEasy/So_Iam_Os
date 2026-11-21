from rest_framework import serializers
from automation.models import WorkflowNode
from automation.api.serializers.action_serializers import ActionSerializer


# ==================================================
# 4️⃣ WorkflowNode (VueFlow Node)
# ==================================================


class WorkflowNodeSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(
        source="program.name", read_only=True
    )
    element_name = serializers.CharField(
        source="element.name", read_only=True
    )
    actions = ActionSerializer(many=True, read_only=True)

    class Meta:
        model = WorkflowNode
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")

    def validate(self, attrs):
        request=self.context.get('request'); workflow=attrs.get('workflow'); program=attrs.get('program'); element=attrs.get('element')
        if request and workflow and workflow.created_by_id != request.user.id: raise serializers.ValidationError({'workflow':'Workflow does not belong to the current user.'})
        if request and program and program.created_by_id != request.user.id: raise serializers.ValidationError({'program':'Program does not belong to the current user.'})
        if request and element and element.created_by_id != request.user.id: raise serializers.ValidationError({'element':'Element does not belong to the current user.'})
        return attrs
