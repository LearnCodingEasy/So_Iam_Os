from personal_finance.models import FinancialAlert
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class FinancialAlertSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = FinancialAlert
        read_only_fields = ["user", "created_at"]
