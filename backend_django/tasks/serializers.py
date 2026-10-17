
from django.utils import timezone
from rest_framework import serializers

from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    status_display = serializers.CharField(
        source="get_status_display",
        read_only=True,
    )
    priority_display = serializers.CharField(
        source="get_priority_display",
        read_only=True,
    )
    overdue = serializers.SerializerMethodField()

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "description",
            "scheduled_date",
            "scheduled_start",
            "due_at",
            "estimated_minutes",
            "actual_minutes",
            "priority",
            "priority_display",
            "status",
            "status_display",
            "sort_order",
            "completed_at",
            "postponed_until",
            "recurrence_rule",
            "metadata",
            "goal",
            "learning_goal",
            "learning_path",
            "learning_topic",
            "skill",
            "overdue",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "status_display",
            "priority_display",
            "overdue",
            "completed_at",
            "created_at",
            "updated_at",
        ]

    def get_overdue(self, obj):
        if obj.status in {
            Task.Status.COMPLETED,
            Task.Status.CANCELLED,
        }:
            return False

        now = timezone.now()
        today = timezone.localdate()

        if obj.due_at:
            due_at = obj.due_at
            if timezone.is_naive(due_at):
                due_at = timezone.make_aware(
                    due_at,
                    timezone.get_current_timezone(),
                )
            return due_at < now

        return bool(
            obj.scheduled_date
            and obj.scheduled_date < today
        )

    def validate_actual_minutes(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Actual minutes cannot be negative."
            )
        return value

    def validate_estimated_minutes(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Estimated minutes cannot be negative."
            )
        return value

    def validate_sort_order(self, value):
        if value is not None and value < 0:
            raise serializers.ValidationError(
                "Sort order cannot be negative."
            )
        return value

    def validate(self, attrs):
        request = self.context.get("request")
        user = getattr(request, "user", None)

        if not user or not user.is_authenticated:
            raise serializers.ValidationError(
                "An authenticated user is required."
            )

        current = self.instance

        def final_value(field):
            if field in attrs:
                return attrs[field]
            return getattr(current, field, None) if current else None

        relations = {
            field: final_value(field)
            for field in (
                "goal",
                "learning_goal",
                "learning_path",
                "learning_topic",
                "skill",
            )
        }

        owner_checks = {
            "goal": lambda obj: getattr(obj, "user_id", None),
            "learning_goal": lambda obj: getattr(
                obj, "user_id", None
            ),
            "learning_path": lambda obj: getattr(
                obj, "user_id", None
            ),
            "learning_topic": lambda obj: getattr(
                getattr(obj, "path", None), "user_id", None
            ),
        }

        for field, get_owner_id in owner_checks.items():
            obj = relations[field]
            if obj is not None and get_owner_id(obj) != user.id:
                raise serializers.ValidationError({
                    field: (
                        "This object does not belong "
                        "to the current user."
                    )
                })

        skill = relations["skill"]
        if skill is not None and not skill.is_active:
            raise serializers.ValidationError({
                "skill": "This skill is inactive."
            })

        learning_path = relations["learning_path"]
        learning_topic = relations["learning_topic"]
        learning_goal = relations["learning_goal"]

        if (
            learning_topic
            and learning_path
            and learning_topic.path_id != learning_path.id
        ):
            raise serializers.ValidationError({
                "learning_topic": (
                    "The topic must belong to the selected path."
                )
            })

        if (
            learning_topic
            and learning_goal
            and learning_topic.path.goal_id != learning_goal.id
        ):
            raise serializers.ValidationError({
                "learning_topic": (
                    "The topic must belong to the selected goal."
                )
            })

        if (
            learning_path
            and learning_goal
            and learning_path.goal_id != learning_goal.id
        ):
            raise serializers.ValidationError({
                "learning_path": (
                    "The path must belong to the selected goal."
                )
            })

        scheduled_date = attrs.get(
            "scheduled_date",
            getattr(current, "scheduled_date", None),
        )
        due_at = attrs.get(
            "due_at",
            getattr(current, "due_at", None),
        )

        if (
            scheduled_date
            and due_at
            and timezone.is_aware(due_at)
            and due_at.date() < scheduled_date
        ):
            raise serializers.ValidationError({
                "due_at": (
                    "The due date cannot precede the scheduled date."
                )
            })

        return attrs
