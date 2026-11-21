from rest_framework import serializers
from personal_finance.models import DebtPayment
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class DebtPaymentSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = DebtPayment
        read_only_fields = ["user"]

    def validate(self, attrs):
        request = self.context["request"]
        debt = attrs.get("debt")
        transaction = attrs.get("transaction")
        if debt and debt.user_id != request.user.id:
            raise serializers.ValidationError({"debt": "Debt does not belong to the current user."})
        if transaction and transaction.user_id != request.user.id:
            raise serializers.ValidationError({"transaction": "Transaction does not belong to the current user."})
        return attrs
