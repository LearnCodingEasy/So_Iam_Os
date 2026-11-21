from rest_framework import serializers
from automation.models import TaskRun


# ==================================================
# 8️⃣ TaskRun
# ==================================================

class TaskRunSerializer(serializers.ModelSerializer):
    workflow_name = serializers.CharField(
        source="workflow.name", read_only=True
    )

    class Meta:
        model = TaskRun
        fields = "__all__"
        read_only_fields = ("id", "started_at", "slug",
                            "created_at", "updated_at", "created_by")
