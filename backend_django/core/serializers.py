from rest_framework import serializers
from .models import UserLearningSettings

class UserLearningSettingsSerializer(serializers.ModelSerializer):
    current_learning_goal_detail = serializers.SerializerMethodField(read_only=True)
    class Meta:
        model = UserLearningSettings
        fields = [
            "daily_learning_tasks", "current_learning_goal", "current_learning_goal_detail",
            "task_generation_enabled", "preferred_learning_time", "updated_at"
        ]
        read_only_fields = ["current_learning_goal_detail", "updated_at"]

    def validate_daily_learning_tasks(self, value):
        if not 1 <= value <= 10:
            raise serializers.ValidationError("Daily learning tasks must be between 1 and 10.")
        return value

    def validate_current_learning_goal(self, value):
        request = self.context.get("request")
        if value is not None and request and value.user_id != request.user.id:
            raise serializers.ValidationError("This learning goal does not belong to you.")
        return value

    def get_current_learning_goal_detail(self, obj):
        goal = obj.current_learning_goal
        if not goal:
            return None
        return {"id": goal.id, "title": goal.title, "status": goal.status, "skill": goal.skill.name if goal.skill else None}
