from rest_framework import serializers
from personal_finance.models import SavingsGoal
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class SavingsGoalSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = SavingsGoal

    def validate(self, attrs):
        goal = attrs.get("general_goal")
        if goal and goal.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"general_goal": "Goal does not belong to the current user."})
        return attrs
