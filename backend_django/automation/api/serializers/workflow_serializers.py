from rest_framework import serializers
from automation.models import Workflow


# ==================================================
# 3️⃣ Workflow
# ==================================================


class WorkflowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Workflow
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")
