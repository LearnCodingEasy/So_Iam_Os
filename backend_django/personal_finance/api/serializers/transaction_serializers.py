from rest_framework import serializers
from personal_finance.models import Transaction
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class TransactionSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = Transaction
        read_only_fields = ["user", "created_at"]

    def validate(self, attrs):
        category = attrs.get("category")
        if category and category.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"category": "Category does not belong to the current user."})
        return attrs
