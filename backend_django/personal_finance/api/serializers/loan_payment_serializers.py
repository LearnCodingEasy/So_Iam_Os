from rest_framework import serializers
from personal_finance.models import LoanPayment
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class LoanPaymentSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = LoanPayment
        read_only_fields = ["user"]

    def validate(self, attrs):
        loan = attrs.get("loan")
        if loan and loan.user_id != self.context["request"].user.id:
            raise serializers.ValidationError({"loan": "Loan does not belong to the current user."})
        return attrs
