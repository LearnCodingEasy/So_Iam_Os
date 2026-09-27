from django.utils import timezone
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(source="get_status_display", read_only=True)
    priority_display = serializers.CharField(source="get_priority_display", read_only=True)
    overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id", "title", "description", "scheduled_date", "scheduled_start", "due_at",
            "estimated_minutes", "actual_minutes", "priority", "priority_display",
            "status", "status_display", "sort_order", "completed_at", "postponed_until",
            "recurrence_rule", "metadata", "goal", "learning_goal", "learning_path",
            "learning_topic", "skill", "overdue", "created_at", "updated_at",
        ]
        read_only_fields = ["id", "status_display", "priority_display", "overdue", "completed_at", "created_at", "updated_at"]

    def get_overdue(self, obj):
        now = timezone.now()
        return bool(
            obj.status not in {Task.Status.COMPLETED, Task.Status.CANCELLED}
            and ((obj.due_at and obj.due_at < now) or (obj.scheduled_date < now.date() and not obj.due_at))
        )

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)
        for field in ("goal", "learning_goal", "learning_path", "learning_topic"):
            obj = attrs.get(field)
            if obj and getattr(obj, "user_id", None) != user.id:
                raise serializers.ValidationError({field: "This object does not belong to the current user."})
        skill = attrs.get("skill")
        if skill and not skill.is_active:
            raise serializers.ValidationError({"skill": "This skill is inactive."})
        return attrs
