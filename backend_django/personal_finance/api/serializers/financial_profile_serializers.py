from personal_finance.models import FinancialProfile
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class FinancialProfileSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = FinancialProfile
        read_only_fields = ["user"]
