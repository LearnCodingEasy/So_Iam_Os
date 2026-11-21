from rest_framework import serializers
from automation.models import Task


# ==================================================
# 7️⃣ Task
# ==================================================


class TaskSerializer(serializers.ModelSerializer):
    program_name = serializers.CharField(
        source="program.name", read_only=True
    )

    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ("id", "slug", "created_at",
                            "updated_at", "created_by")
