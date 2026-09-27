from rest_framework import serializers

from .models import Goal


class GoalSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display", read_only=True)
    priority_display = serializers.CharField(
        source="get_priority_display", read_only=True)
    task_count = serializers.IntegerField(read_only=True)
    completed_task_count = serializers.IntegerField(read_only=True)
    overdue = serializers.SerializerMethodField()

    class Meta:
        model = Goal
        fields = [
            "id", "title", "description", "priority", "priority_display",
            "status", "status_display", "start_date", "target_date",
            "estimated_minutes", "actual_minutes", "progress_percent",
            "completion_notes", "completed_at", "metadata", "learning_goals",
            "skills", "task_count", "completed_task_count", "overdue",
            "created_at", "updated_at",
        ]
        read_only_fields = [
            "id", "status_display", "priority_display", "task_count",
            "completed_task_count", "overdue", "completed_at", "created_at",
            "updated_at",
        ]

    def get_overdue(self, obj):
        from django.utils import timezone
        return bool(
            obj.target_date
            and obj.target_date < timezone.localdate()
            and obj.status not in {Goal.Status.COMPLETED, Goal.Status.CANCELLED, Goal.Status.ARCHIVED}
        )

    def validate(self, attrs):
        start = attrs.get("start_date", getattr(
            self.instance, "start_date", None))
        target = attrs.get("target_date", getattr(
            self.instance, "target_date", None))
        if start and target and target < start:
            raise serializers.ValidationError(
                {"target_date": "Target date cannot be before start date."})
        return attrs
