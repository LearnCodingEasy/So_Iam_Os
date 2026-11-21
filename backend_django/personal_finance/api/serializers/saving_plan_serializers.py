from rest_framework import serializers
from personal_finance.models import SavingPlan
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class SavingPlanSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = SavingPlan
        read_only_fields = ["user"]

    def validate(self, attrs):
        goal = attrs.get("goal")
        if goal and goal.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"goal": "Goal does not belong to the current user."})
        return attrs
