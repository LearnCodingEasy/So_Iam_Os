from personal_finance.models import FinancialScenario
from personal_finance.api.serializers.owned_model_serializers import OwnedModelSerializer


class FinancialScenarioSerializer(OwnedModelSerializer):
    class Meta(OwnedModelSerializer.Meta):
        model = FinancialScenario
        read_only_fields = ["user", "created_at", "result"]
