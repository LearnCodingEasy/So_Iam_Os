from rest_framework import serializers
from automation.models import WorkflowEdge


# ==================================================
# 5️⃣ WorkflowEdge
# ==================================================

class WorkflowEdgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkflowEdge
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")
